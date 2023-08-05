import numpy
import pfft
import mpsort
from . import domain
from . import window
from mpi4py import MPI

import numbers # for testing Numbers

class slabiter(object):
    def __init__(self, field):
        # we iterate over the slowest axis to gain locality.
        axissort = numpy.argsort(field.value.strides)[::-1]
        axis = axissort[0]

        self.optimized_view = field.value.transpose(axissort)
        self.nslabs = field.shape[axis]

        optx = [xx.transpose(axissort) for xx in field.x]
        opti = [ii.transpose(axissort) for ii in field.i]
        self.x = xslabiter(axis, self.nslabs, optx)
        self.i = xslabiter(axis, self.nslabs, opti)

    def __iter__(self):
        for irow in range(self.nslabs):
            yield self.optimized_view[irow]

class xslabiter(slabiter):
    def __init__(self, axis, nslabs, optx):
        self.axis = axis
        self.nslabs = nslabs
        self.optx = optx

    def __iter__(self):
        for irow in range(self.nslabs):
            kk = [x[0] if d != self.axis else x[irow] for d, x in enumerate(self.optx)]
            yield kk


class Field(object):
    """ Base class for RealField and ComplexField.

        It only supports those two subclasses.
    """
    def copy(self):
        other = self.__class__(self.pm)
        other.value[...] = self.value
        return other

    def __init__(self, pm, base=None):
        """ Used internally to add shortcuts of attributes from pm """
        if base is None:
            base = pfft.LocalBuffer(pm.partition)
        self.base = base
        self.pm = pm
        self.partition = pm.partition
        self.BoxSize = pm.BoxSize
        self.Nmesh = pm.Nmesh
        if isinstance(self, RealField):
            self.value = self.base.view_input()
            self.start = self.partition.local_i_start
            self.global_shape = pm.Nmesh
            self.x = pm.x
            self.i = pm.i_ind
        elif isinstance(self, ComplexField):
            self.value = self.base.view_output()
            self.start = self.partition.local_o_start
            self.global_shape = pm.Nmesh.copy()
            self.global_shape[-1] = self.global_shape[-1] // 2 + 1
            self.x = pm.k
            self.i = pm.o_ind
            self.real = self.value.real
            self.imag = self.value.imag
            self.plain = self.value.view(dtype=(self.real.dtype, 2))
        else:
            raise TypeError("Olny RealField and ComplexField. No more subclassing");

        # copy over a few ndarray attributes
        self.flat = self.value.flat

        self.shape = self.value.shape
        self.size = self.value.size
        self.dtype = self.value.dtype

        # the slices in the full array 
        self.slices = tuple([
                slice(s, s + n)
                for s, n in zip(self.start, self.shape)
                ])

        self.csize = pm.comm.allreduce(self.size)

    def __getitem__(self, index):
        return self.value.__getitem__(index)

    def __setitem__(self, index, value):
        return self.value.__setitem__(index, value)

    def __array__(self, dtype=None):
        return self.value

    @property
    def slabs(self):
        return slabiter(self)

    def sort(self, out=None):
        """ Sort the field to 'C'-order, partitioned by MPI ranks. Save the
            result to flatiter.

            Parameters
            ----------
            out : numpy.flatiter
                A flatiter to store the 'C' order. If not a flatiter, the .flat
                attribute is used.

            Returns
            -------
            numpy.flatiter : the flatiter provided or created.

            Notes
            -----
            Set `out` to self.value for an 'inplace' sort.
        """
        ind = numpy.ravel_multi_index(numpy.mgrid[self.slices], self.global_shape)

        if out is None:
            out = numpy.empty_like(self.value)

        if not isinstance(out, numpy.flatiter):
            out = out.flat

        assert isinstance(out, numpy.flatiter)
        assert len(out) == self.size

        return mpsort.sort(self.flat, orderby=ind.flat, comm=self.pm.comm, out=out)

    def unsort(self, flatiter):
        """ Unsort c-ordered field values to the field.

            Parameters
            ----------
            flatiter : numpy.flatiter

            Notes
            -----
            self is updated. `array` does not have to be C_CONTIGUOUS flat iterator of array is used.
        """
        if not isinstance(flatiter, numpy.flatiter):
            flatiter = flatiter.flat

        assert isinstance(flatiter, numpy.flatiter)
        assert len(flatiter) == self.size

        ind = numpy.ravel_multi_index(numpy.mgrid[self.slices], self.global_shape)
        mpsort.permute(flatiter, argindex=ind.flat, comm=self.pm.comm, out=self.flat)

    def resample(self, out):
        """ Resample the Field by filling 0 or truncating modes.
            Convert from and between Real/Complex automatically.

            Parameters
            ----------
            out : Field
                must be provided because it is a different PM. Can be RealField or ComplexField

        """
        assert isinstance(out, Field)

        if all(out.Nmesh == self.Nmesh):
            # no resampling needed. Just do Fourier transforms.
            if isinstance(self, RealField) and isinstance(out, ComplexField):
                self.r2c(out)
            if isinstance(self, RealField) and isinstance(out, RealField):
                out.value[...] = self.value
            if isinstance(self, ComplexField) and isinstance(out, RealField):
                self.c2r(out)
            if isinstance(self, ComplexField) and isinstance(out, ComplexField):
                out.value[...] = self.value
            return out

        if isinstance(self, RealField):
            self = self.r2c()

        if isinstance(out, RealField):
            complex = ComplexField(out.pm)
        else:
            complex = out

        complex.value[...] = 0.0

        tmp = numpy.empty_like(self.value)

        self.sort(out=tmp)

        # indtable stores the index in pmsrc for the mode in pmdest
        # since pmdest < pmsrc, all items are alright.
        indtable = [reindex(self.Nmesh[d], out.Nmesh[d]) for d in range(self.value.ndim)]

        ind = build_index(
                [t[numpy.r_[s]]
                for t, s in zip(indtable, complex.slices) ],
                self.global_shape)

        # fill the points that has values in pmsrc
        mask = ind >= 0
        # their indices
        argind = ind[mask]
        # take the data

        data = mpsort.take(tmp.flat, argind, self.pm.comm)

        # fill in the value
        complex[mask] = data

        # ensure the down sample is real
        for i, slab in zip(complex.slabs.i, complex.slabs):
            mask = numpy.ones(slab.shape, '?')
            for ii, n in zip(i, complex.Nmesh):
               mask &= (n - ii) % n == ii
            slab.imag[mask] = 0

        if isinstance(out, RealField):
            complex.c2r(out)

        return out

class RealField(Field):
    def __init__(self, pm, base=None):
        Field.__init__(self, pm, base)

    def r2c(self, out=None):
        """ 
        Perform real to complex transformation.

        """
        if out is None:
            out = ComplexField(self.pm)

        if out is self:
            out = ComplexField(self.pm, base=self.base)

        assert isinstance(out, ComplexField)

        if self.base is out.base:
            self.pm.ipforward.execute(self.base, out.base)
        else:
            self.pm.forward.execute(self.base, out.base)

        # PFFT normalization, same as FastPM
        out.value[...] *= numpy.prod(self.pm.Nmesh ** -1.0)

        return out

    def csum(self):
        """ Collective mean. Sum of the entire mesh. (Must be called collectively)"""
        return self.pm.comm.allreduce(self.value.sum(dtype='f8'))

    def cmean(self):
        """ Collective mean. Mean of the entire mesh. (Must be called collectively)"""
        return self.csum() / self.csize

    def paint(self, pos, mass=1.0, method=None, transform=None, hold=False, gradient=None):
        """ 
        Paint particles into the internal real canvas. 

        Transform the particle field given by pos and mass
        to the overdensity field in fourier space and save
        it in the internal storage. 
        A multi-linear CIC approximation scheme is used.

        The function can be called multiple times: 
        the result is cummulative. In a multi-step simulation where
        :py:class:`ParticleMesh` object is reused,  before calling 
        :py:meth:`paint`, make sure the canvas is cleared with :py:meth:`clear`.

        Parameters
        ----------
        pos    : array_like (, ndim)
            position of particles in simulation unit

        mass   : scalar or array_like (,)
            mass of particles in simulation unit

        hold   : bool
            If true, do not clear the current value in the field.

        gradient : None or integer
            Direction to take the gradient of the window. The affine transformation
            is properly applied.

        method: None or string
            type of window. Default : None, use self.pm.method

        Notes
        -----
        the painter operation conserves the total mass. It is not the density.

        """
        # Transform from simulation unit to local grid unit.
        if not transform:
            transform = self.pm.affine

        if method is None:
            method = self.pm.method

        if method in window.methods:
            method = window.methods[method]

        if not hold:
            self.value[...] = 0

        method.paint(self.value, pos, mass, transform=transform, diffdir=gradient)

    def readout(self, pos, out=None, method=None, transform=None, gradient=None):
        """ 
        Read out from real field at positions

        Parameters
        ----------
        pos    : array_like (, ndim)
            position of particles in simulation  unit
        gradient : None or integer
            Direction to take the gradient of the window. The affine transformation
            is properly applied.
        method : None or string
            type of window, default to self.pm.method

        Returns
        -------
        rt     : array_like (,)
            read out values from the real field.

        """
        if not transform:
            transform = self.pm.affine

        if method is None:
            method = self.pm.method

        if method in window.methods:
            method = window.methods[method]

        return method.readout(self.value, pos, out=out, transform=transform, diffdir=gradient)

    def readout_gradient(self, pos, btgrad, method=None, transform=None, gradient=None, return_pos=False):
        """ back-propagate the gradient of readout to self.

            Parameters
            ----------
            btgrad : array
                current gradient over a readout.

            return_pos: boolean
                Returns the gradient over position.

        """
        if return_pos:
            if gradient is not None:
                raise ValueError("gradient of gradient is not yet supported")
            pos_grad = numpy.zeros_like(pos)
            for d in range(pos.shape[1]):
                self.readout(pos, out=pos_grad[:, d], method=method, transform=transform, gradient=d)
                pos_grad[:, d] *= btgrad

        self_grad = RealField(self.pm)
        self_grad.paint(pos, mass=btgrad, method=method, transform=transform, gradient=gradient, hold=False)

        if return_pos:
            return self_grad, pos_grad

        return self_grad

    def paint_gradient(self, pos, weights, method=None, transform=None, gradient=None,
            return_pos=False, return_weights=True):
        """ back-propagate the gradient of paint from self. self contains
            the current gradient.

            Parameters
            ----------
            return_pos: boolean
                Returns the gradient over position.

            return_weights: boolean
                Returns the gradient over position.

        """
        if return_pos:
            if gradient is not None:
                raise ValueError("gradient of gradient is not yet supported")
            pos_grad = numpy.zeros_like(pos)
            for d in range(pos.shape[1]):
                self.readout(pos, out=pos_grad[:, d], method=method, transform=transform, gradient=d)

        if return_weights:
            weights_grad = numpy.zeros_like(weights)
            self.readout(pos, out=weights_grad, method=method, transform=transform, gradient=gradient)
            weights_grad[...] *= weights

        if return_pos and return_weights:
            return pos_grad, weights_grad

        if return_pos:
            return pos_grad

        if return_weights:
            return weights_grad

    def r2c_gradient(self, btgrad):
        """ Back-propagate the gradient of r2c to self. """
        btgrad.c2r(self)
        # PFFT normalization, same as FastPM
        self.value[...] *= numpy.prod(self.pm.Nmesh ** -1.0)

    def apply(self, func, kind="relative"):
        """ apply a function to the field, in-place.

            Parameters
            ----------
            func : callable
                func(r, v) where r is a list of r values that broadcasts into a full array.
                value of r depends on kind. v is the value of the field on the corresponding locations.
            kind : string
                The kind of value in r.
                'relative' means distance from [-0.5 Boxsize, 0.5 BoxSize).
                'index' means [0, Nmesh )
        """
        for x, i, slab in zip(self.slabs.x, self.slabs.i, self.slabs):
            if kind == 'relative':
                slab[...] = func(x, slab)
            elif kind == 'index':
                slab[...] = func(i, slab)
            else:
                raise ValueError("kind is relative, or index")

class ComplexField(Field):
    def __init__(self, pm, base=None):
        Field.__init__(self, pm, base)

    def c2r(self, out=None):
        if out is None:
            out = RealField(self.pm)
        if out is self:
            out = RealField(self.pm, self.base)

        assert isinstance(out, RealField)
        if out.base is not self.base:
            self.pm.backward.execute(self.base, out.base)
        else:
            self.pm.ipbackward.execute(self.base, out.base)

        return out

    def c2r_gradient(self, btgrad):
        """ Back-propagate the gradient of c2r to self. """
        btgrad.r2c(self)
        # PFFT normalization, same as FastPM
        self.value[...] *= numpy.prod(self.pm.Nmesh ** 1.0)

    def decompress_gradient(self, btgrad):
        """ Back-propagate the gradient of decompress to self. """
        assert isinstance(btgrad, ComplexField)
        for i, a, b in zip(btgrad.slabs.i, self.slabs, btgrad.slabs):
            # modes that are self conjugates do not gain a factor
            mask = numpy.ones(a.shape, '?')
            for ii, n in zip(i, btgrad.Nmesh):
               mask &= (n - ii) % n == ii
            a[~mask] = 2 * b[~mask]
            a[mask] = b[mask]
    def generate_whitenoise(self, seed):
        """ Generate white noise to the field with the given seed.

            The scheme is supposed to be compatible with Gadget. The field must be three-dimensional.
        """
        assert len(self.shape) == 3

        from .whitenoise import generate
        generate(self.value, self.start, self.Nmesh, seed)

    def apply(self, func, kind="wavenumber"):
        """ apply a function to the field, in-place.

            Parameters
            ----------
            func : callable
                func(k, v) where k is a list of k values that broadcasts into a full array.
                value of k depends on kind. v is the corrsponding value of field.
            kind : string
                The kind of value in k.
                'wavenumber' means wavenumber from [- 2 pi / L * N / 2, 2 pi / L * N / 2).
                'circular' means circular frequency from [- pi, pi).
                'index' means [0, Nmesh )
        """
        for k, i, slab in zip(self.slabs.x, self.slabs.i, self.slabs):
            if kind == 'wavenumber':
                slab[...] = func(k, slab)
            elif kind == 'circular':
                w = [ ki * L / N for ki, L, N in zip(k, self.BoxSize, self.Nmesh)]
                slab[...] = func(w, slab)
            elif kind == 'index':
                slab[...] = func(i, slab)
            else:
                raise ValueError("kind is wavenumber, circular, or index")

def build_index(indices, fullshape):
    """
        Build a linear index array based on indices on an array of fullshape.
        This is similar to numpy.ravel_multi_index.

        index value of -1 will on any axes will be translated to -1 in the final.

        Parameters:
            indices : a tuple of index per dimension.

            fullshape : a tuple of the shape of the full array

        Returns:
            ind : a 3-d array of the indices of the coordinates in indices in
                an array of size fullshape. -1 if any indices is -1.

    """
    localshape = [ len(i) for i in indices]
    ndim = len(localshape)
    ind = numpy.zeros(localshape, dtype='i8')
    for d in range(len(indices)):
        i = indices[d]
        i = i.reshape([-1 if dd == d else 1 for dd in range(ndim)])
        ind[...] *= fullshape[d]
        ind[...] += i

    mask = numpy.zeros(localshape, dtype='?')

    # now mask out bad points by -1
    for d in range(len(indices)):
        i = indices[d]
        i = i.reshape([-1 if dd == d else 1 for dd in range(ndim)])
        mask |= i == -1

    ind[mask] = -1
    return ind

def reindex(Nsrc, Ndest):
    """ returns the index in the frequency array for corresponding
        k in Nsrc and composes Ndest

        For those Ndest that doesn't exist in Nsrc, return -1

        Example:
        >>> reindex(8, 4)
        >>> array([0, 1, 2, 7])
        >>> reindex(4, 8)
        >>> array([ 0,  1,  2, -1, -1, -1,  -1,  3])

    """
    reindex = numpy.arange(Ndest)
    reindex[Ndest // 2 + 1:] = numpy.arange(Nsrc - Ndest // 2 + 1, Nsrc, 1)
    reindex[Nsrc // 2 + 1: Ndest -Nsrc //2 + 1] = -1
    return reindex

class ParticleMesh(object):
    """
    ParticleMesh provides an interface to solver for forces
    with particle mesh method

    ParticleMesh does not deal with memory. Use RealField(pm) and ComplexField(pm)
    to create memory buffers.

    Attributes
    ----------
    np      : array_like (npx, npy)
        The shape of the process mesh. This is the number of domains per direction.
        The product of the items shall equal to the size of communicator. 
        For example, for 64 rank job, np = (8, 8) is a good choice.
        Since for now only 3d simulations are supported, np must be of length-2.
        The default is try to split the total number of ranks equally. (eg, for
        a 64 rank job, default is (8, 8)

    comm    : :py:class:`MPI.Comm`
        the MPI communicator, (default is MPI.COMM_WORLD)

    Nmesh   : array of int
        number of mesh points per side. The length decides the number of dimensions.

    BoxSize : float
        size of box

    domain   : :py:class:`pmesh.domain.GridND`
        domain decomposition (private)

    partition : :py:class:`pfft.Partition`
        domain partition (private)

    w   : list
        a list of the circular frequencies along each direction (-pi to pi)
    k   : list
        a list of the wave numbers k along each direction (- pi N/ L to pi N/ L)
    x   : list
        a list of the position along each direction (-L/2 to L/ 2). x is conjugate of k.
    r   : list
        a list of the mesh position along each direction (-N/2 to N/2). r is conjugate of w.

    """

    def __init__(self, Nmesh, BoxSize=1.0, comm=None, np=None, dtype='f8', plan_method='estimate', method='cic'):
        """ create a PM object.  """
        if comm is None:
            comm = MPI.COMM_WORLD

        self.comm = comm

        if np is None:
            if len(Nmesh) >= 3:
                np = pfft.split_size_2d(self.comm.size)
            else:
                np = [self.comm.size]

        dtype = numpy.dtype(dtype)
        if dtype is numpy.dtype('f8'):
            forward = pfft.Type.PFFT_R2C
            backward = pfft.Type.PFFT_C2R
        elif dtype is numpy.dtype('f4'):
            forward = pfft.Type.PFFTF_R2C
            backward = pfft.Type.PFFTF_C2R
        else:
            raise ValueError("dtype must be f8 or f4")

        self.procmesh = pfft.ProcMesh(np, comm=comm)
        self.Nmesh = numpy.array(Nmesh, dtype='i8')
        self.BoxSize = numpy.empty(len(Nmesh), dtype='f8')
        self.BoxSize[:] = BoxSize
        self.partition = pfft.Partition(forward,
            self.Nmesh,
            self.procmesh,
            pfft.Flags.PFFT_TRANSPOSED_OUT | pfft.Flags.PFFT_PADDED_R2C)

        bufferin = pfft.LocalBuffer(self.partition)
        bufferout = pfft.LocalBuffer(self.partition)

        plan_method = {
            "estimate": pfft.Flags.PFFT_ESTIMATE,
            "measure": pfft.Flags.PFFT_MEASURE,
            "exhaustive": pfft.Flags.PFFT_EXHAUSTIVE,
            } [plan_method]

        self.forward = pfft.Plan(self.partition, pfft.Direction.PFFT_FORWARD,
                bufferin, bufferout, forward,
                plan_method | pfft.Flags.PFFT_TRANSPOSED_OUT | pfft.Flags.PFFT_TUNE | pfft.Flags.PFFT_PADDED_R2C)
        self.backward = pfft.Plan(self.partition, pfft.Direction.PFFT_BACKWARD,
                bufferout, bufferin, backward, 
                plan_method | pfft.Flags.PFFT_TRANSPOSED_IN | pfft.Flags.PFFT_TUNE | pfft.Flags.PFFT_PADDED_C2R)

        self.ipforward = pfft.Plan(self.partition, pfft.Direction.PFFT_FORWARD,
                bufferin, bufferin, forward,
                plan_method | pfft.Flags.PFFT_TRANSPOSED_OUT | pfft.Flags.PFFT_TUNE | pfft.Flags.PFFT_PADDED_R2C)
        self.ipbackward = pfft.Plan(self.partition, pfft.Direction.PFFT_BACKWARD,
                bufferout, bufferout, backward, 
                plan_method | pfft.Flags.PFFT_TRANSPOSED_IN | pfft.Flags.PFFT_TUNE | pfft.Flags.PFFT_PADDED_C2R)

        self.domain = domain.GridND(self.partition.i_edges, comm=self.comm)

        k = []
        x = []
        w = []
        r = []
        o_ind = []
        i_ind = []

        for d in range(self.partition.ndim):
            t = numpy.ones(self.partition.ndim, dtype='intp')
            s = numpy.ones(self.partition.ndim, dtype='intp')
            t[d] = self.partition.local_i_shape[d]
            s[d] = self.partition.local_o_shape[d]

            i_indi = numpy.arange(t[d], dtype='intp') + self.partition.local_i_start[d]
            o_indi = numpy.arange(s[d], dtype='intp') + self.partition.local_o_start[d]

            wi = numpy.arange(s[d], dtype='f4') + self.partition.local_o_start[d] 
            ri = numpy.arange(t[d], dtype='f4') + self.partition.local_i_start[d] 

            wi[wi >= self.Nmesh[d] // 2] -= self.Nmesh[d]
            ri[ri >= self.Nmesh[d] // 2] -= self.Nmesh[d]

            wi *= (2 * numpy.pi / self.Nmesh[d])
            ki = wi * self.Nmesh[d] / self.BoxSize[d]
            xi = ri * self.BoxSize[d] / self.Nmesh[d]

            o_ind.append(o_indi.reshape(s))
            i_ind.append(i_indi.reshape(t))
            w.append(wi.reshape(s))
            r.append(ri.reshape(t))
            k.append(ki.reshape(s))
            x.append(xi.reshape(t))

        self.i_ind = i_ind
        self.o_ind = o_ind
        self.w = w
        self.r = r
        self.k = k
        self.x = x

        # Transform from simulation unit to local grid unit.
        self.affine = window.Affine(self.partition.ndim,
                    translate=-self.partition.local_i_start,
                    scale=1.0 * self.Nmesh / self.BoxSize,
                    period = self.Nmesh)

        if method in window.methods:
            method = window.methods[method]
        self.method = method

    def decompose(self, pos, smoothing=None):
        """ 
        Create a domain decompose layout for particles at given
        coordinates.

        Parameters
        ----------
        pos    : array_like (, ndim)
            position of particles in simulation  unit

        smoothing : None, float, string, or ResampleWindow
            if given as a string or ResampleWindow, use 0.5 * support.
            This is the size of the buffer region around a domain.
            Default: None, use self.method

        Returns
        -------
        layout  : :py:class:domain.Layout
            layout that can be used to migrate particles and images
        to the correct MPI ranks that hosts the PM local mesh
        """
        if smoothing is None:
            smoothing = self.method

        if smoothing in window.methods:
            smoothing = window.methods[smoothing]

        if isinstance(smoothing, window.ResampleWindow):
            smoothing = smoothing.support * 0.5

        assert isinstance(smoothing, numbers.Number)

        # Transform from simulation unit to global grid unit.
        def transform0(x):
            return self.affine.scale * x

        return self.domain.decompose(pos, smoothing=smoothing,
                transform=transform0)
