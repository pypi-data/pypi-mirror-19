import numpy as np
from numpy.fft import fftn, ifftn, ifftshift, fftshift, fftfreq



class PowerBox(object):
    def __init__(self,N,pk, dim=2, transform=None, boxlength=1.0,angular_freq=True,
                 keep_pretransform=False, gauss_width=1):
        """
        An object which calculates and stores the real-space and fourier-space fields generated with a given power
        spectrum.

        Parameters
        ----------
        N : int
            Number of grid-points on a side for the resulting box (equivalently, number of wavenumbers to use).

        pk : func
            A function of a single (vector) variable k, which is the isotropic power spectrum.

        dim : int, default 2
            Number of dimensions of resulting box.

        transform : string or None, {None,"lognormal","physical"}
            The output densities by default form a Gaussian distribution. This can be transformed to a log-normal
            distribution, or can be clipped at -1 with the "physical" option (preserving physical interpretation of
            the signal being overdensities).

        boxlength : float, default 1.0
            Length of the final signal on a side.

        angular_freq : bool, default `True`
            Whether the fourier-dual of `x` (called `k` in this code) is an angular frequency (i.e. k = 2pi/x) or not
            (i.e. k = 1/x).

        keep_pretransform : bool, default `False`
            Whether to keep the original (gaussian) signal in memory.

        Attributes
        ----------
        delta_k : array
            An array, with `dim` dimensions, representing the fourier-space signal.

        delta_x : array
            An array, with `dim` dimensions, representing the real-space signal.

        delta_x_gauss : array
            An array, with `dim` dimensions, representing the real-space signal as the original gaussian field, before
            log-normal or clip transformations.

        Notes
        -----
        A number of conventions need to be listed.

        The conventions of using `x` for "real-space" and `k` for "fourier space" arise from cosmology, but this does
        not affect anything -- `x` could just as well stand for "time domain" and `k` for "frequency domain".

        The important convention is the relationship between `x` and `k`, or in other words, whether `k` is interpreted
        as an angular frequency or ordinary frequency. By default, because of cosmological conventions, `k` is an
        angular frequency, so that the fourier transform integrand is delta_k*exp(-ikx).

        The normalisation of the FT is set so as to return a statistically invariant real-space field with respect to
        the resolution of the grid. That is, increasing the resolution does not change the variance of the resulting
        field on a given scale. Again, this conforms to physical expectation in terms of cosmological usage.

        The returned box has (expected) mean zero. This enables its direct interpretation as a cosmological overdensity
        field.

        Examples
        --------
        To create a 3-dimensional box of gaussian over-densities, with side length 1 Mpc, gridded equally into
        100 bins, and where k=2pi/x, with a power-law power spectrum, simply use

        >>> pb = PowerBox(100,lambda k : 0.1*k**-3., dim=3,boxlength=100.0)
        >>> overdensities = pb.delta_x
        >>> grid = pb.x
        >>> radii = pb.r

        To create a 2D turbulence structure, with arbitrary units, once can use

        >>> import matplotlib.pyplot as plt
        >>> pb = PowerBox(1000, lambda k : k**-7./5.)
        >>> plt.imshow(pb.delta_x)

        To create a log-normal overdensity field, use

        >>> pb = PowerBox(100, lambda k : 0.1*k**-2.5, boxlength=100.0, transform='lognormal')
        """

        self.N = N
        self.dim = dim
        self.boxlength = boxlength
        self.L = boxlength
        self.angular_freq = angular_freq
        self.transform = transform
        self.pk = pk

        # Our algorithm at this point only deals with even-length arrays.
        # assert N%2 == 0
        if N%2 == 0:
            self._even = True
        else:
            self._even = False

        self.n = N + 1 if self._even else N

        # Get the grid-size for the final real-space box.
        self.dx = float(boxlength)/N

#         mag = np.ones(shape=[n]*dim)
# #        mag = np.random.normal(0, gauss_width, size=[n]*dim)
#         pha = 2*np.pi*np.random.uniform(size=[n]*dim)
#
#         self.delta_k = self._make_hermitian(mag,pha)
#
#         if self._even:
#             cutidx = [slice(None,-1)]*dim
#             self.delta_k = self.delta_k[cutidx]

        # Generate the (sqrt) power spectrum based on k (not K!)
        # dk = self.gauss_hermitian
        #
        # k = self.k
        # P = np.zeros_like(k)
        # P[k != 0] = np.sqrt(pk(k[k != 0]))

        # Multiply the k-space random numbers with the sqrt power.
        self.delta_k = np.sqrt(self.power_array) * self.gauss_hermitian

        # Finally, get the realspace, by inverse FT of kspace.
        # Note we ifftshift kspace, to get the zero as the first element as numpy expects.
        self.delta_x = np.real(N ** dim*ifftn(ifftshift(self.delta_k)))

        if keep_pretransform and not transform:
            self.delta_x_gauss = self.delta_x.copy()
        elif keep_pretransform and transform:
            self.delta_x_gauss = self.delta_x

        if transform=="lognormal":
            self.delta_x = np.exp(self.delta_x)
        elif transform=="physical":
            np.clip(self.delta_x,-1,np.inf,self.delta_x)


    @property
    def k(self):
        "The entire grid of wavenumber magitudes"
        # Create K, the frequencies that numpy implicity uses when summing over frequency bins

        k = self.kvec ** 2
        K = self.kvec ** 2
        for i in range(self.dim - 1):
            k = np.add.outer(K, k)
        return np.sqrt(k)

    @property
    def kvec(self):
        "The vector of wavenumbers along a side"
        # Create K, the frequencies that numpy implicity uses when summing over frequency bins
        A = 2*np.pi if self.angular_freq else 1
        return A*fftshift(fftfreq(self.N, d=self.dx))

    @property
    def r(self):
        "The radial position of every point in the grid"
        X = self.x**2
        x = self.x**2
        for i in range(self.dim - 1):
            x = np.add.outer(X, x)
        return np.sqrt(x)

    @property
    def x(self):
        "The co-ordinates of the grid along a side"
        if self._even:
            return np.arange(-self.N/2.,self.N/2.)*self.dx
        else:
            return np.linspace(-self.boxlength, self.boxlength,self.N)

    @property
    def gauss_hermitian(self):
        mag = np.ones(shape=[self.n]*self.dim)
        #        mag = np.random.normal(0, gauss_width, size=[n]*dim)
        pha = 2*np.pi*np.random.uniform(size=[self.n]*self.dim)

        dk = self._make_hermitian(mag, pha)

        if self._even:
            cutidx = [slice(None, -1)]*self.dim
            dk = dk[cutidx]

        return dk

    @property
    def power_array(self):
        k = self.k
        P = np.zeros_like(k)
        P[k != 0] = self.pk(k[k != 0])
        return P

    def _make_hermitian(self,mag,pha):
        """
        Take random arrays and convert them to a complex hermitian array.

        Note that this assumes that mag is distributed normally.

        Parameters
        ----------
        mag : array
            Normally-distributed magnitudes of the complex vector.

        pha : array
            Uniformly distributed phases of the complex vector

        Returns
        -------
        kspace : array
            A complex hermitian array with normally distributed amplitudes.
        """
        revidx = [slice(None,None,-1)]*len(mag.shape)
        mag = (mag + mag[revidx])/np.sqrt(2)
        pha = (pha - pha[revidx])/2 + np.pi
        return mag*(np.cos(pha) + 1j*np.sin(pha))

    def create_discrete_sample(self,nbar):
        """
        Assuming that the real-space signal represents an over-density with respect to some mean, create a sample
        of tracers of the underlying density distribution.

        Parameters
        ----------
        nbar : float
            Mean tracer density within the box.
        """
        if not self.transform:
            delx = np.clip(self.delta_x,-1,np.inf)
        else:
            delx = self.delta_x

        n = (delx + 1)*self.dx ** self.dim * nbar
        self.n_per_cell = np.random.poisson(n)

        # Get all source positions
        X, Y, Z = np.meshgrid(self.x, self.x, self.x)

        self.tracer_positions = np.array([X.flatten(), Y.flatten(), Z.flatten()]).T
        self.tracer_positions = self.tracer_positions.repeat(self.n_per_cell.flatten(), axis=0) + np.random.uniform(size=(np.sum(self.n_per_cell), 3))*self.dx

        return self.tracer_positions


def get_power(x,k):
    """
    Calculate the n-ball-averaged power spectrum of a given field.

    Parameters
    ----------
    x : array-like
        The field to calculate the power spectrum of. Can be arbitrarily n-dimensional, but each dimension
        should have the same size.

    k : array-like
        An array of the same shape as `x`, defining the absolute value of the wavenumber at each position of the
        (inverted) grid.

    Returns
    -------
    p_k : array
        The power spectrum averaged over bins of equal |k|.

    centres : array
        The bin-centres for the p_k array (in k).

    Examples
    --------
    One can use this function to check whether a box created with :class:`PowerBox` has the correct
    power spectrum:

    >>> from powerbox import PowerBox, get_power
    >>> import matplotlib.pyplot as plt
    >>> pb = PowerBox(250,lambda k : k**-2.)
    >>> p,k = get_power(pb.delta_x,pb.k)
    >>> plt.plot(k,p)
    >>> plt.plot(k,k**-2.)
    >>> plt.xscale('log')
    >>> plt.yscale('log')
    """

    P = np.abs(fftshift(fftn(x)/len(x)**len(x.shape)))**2

    hist1 = np.histogram(k.flatten(),bins=int(len(k)/2.2))[0]
    hist,edges = np.histogram(k.flatten(),bins=int(len(k)/2.2),weights=P.flatten())

    p_k = hist/hist1
    centres = (edges[1:]+edges[:-1])/2
    return p_k, centres
