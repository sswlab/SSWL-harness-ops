"""
Interpolate AIA temperature response functions to user-defined bins.

Given user choice of channels, number of temperature bins, a logarithmic
temperature range, and AIA response data, this procedure interpolates
the response profiles and estimates uncertainties.

Reference:
    Morgan, H. 2019, Sol Phys, 294, 135
    https://ui.adsabs.harvard.edu/abs/2019SoPh..294..135M/abstract
"""

import numpy as np
from scipy.interpolate import interp1d


def dem_aiainterpolresponse_sites(wavel, nout, logtempra, response_structure,
                                   reglog=False):
    """Interpolate AIA response functions to user-defined temperature bins.

    Parameters
    ----------
    wavel : array_like
        Required wavelength channels and their order,
        e.g. [94, 131, 171, 193, 211, 304, 335].
    nout : int
        Required number of output temperature bins, e.g. 41.
    logtempra : array_like, length 2
        [min, max] of log10(T) range, e.g. [5.7, 7.0].
    response_structure : dict
        Structure with keys:
        - 'logte': array of log10(T) values
        - 'channels': list of channel name strings (e.g. 'A94', 'A131', ...)
        - 'all': 2-D response array, shape (ntemp, nchannel)
    reglog : bool, optional
        If True, use regular logarithmic temperature scale.
        If False (default), regular in linear temperature.

    Returns
    -------
    dict with keys:
        'logte_out'    : ndarray, shape (nout,) — log10(T) at each output bin
        'response_out' : ndarray, shape (nout, nwl) — interpolated response
        'reserr'       : ndarray, shape (nwl,) — relative response error
        'dtemp'        : ndarray, shape (nout,) — temperature bin widths [K]
    """
    wavel = np.asarray(wavel, dtype=np.int64)
    logtempra = np.asarray(logtempra, dtype=np.float64)
    nwl = len(wavel)

    logte_full = np.asarray(response_structure['logte'], dtype=np.float64)
    resp_all = np.asarray(response_structure['all'], dtype=np.float64)

    # Extract channel names → wavelength integers
    channels = response_structure['channels']
    wlall = np.array([int(ch[1:]) for ch in channels], dtype=np.int64)

    # Temperature range selection
    ntin_full = len(logte_full)
    dt0 = np.gradient(10.0 ** logte_full)  # derivative d(10^logte)/d(index)

    indtemp = np.where((logte_full >= logtempra[0]) &
                       (logte_full <= logtempra[1]))[0]
    nindtemp = np.where((logte_full < logtempra[0]) |
                        (logte_full > logtempra[1]))[0]
    ncomp = len(nindtemp)
    ntemp = len(indtemp)

    logte_in = logte_full[indtemp]

    # Extract response for each requested channel
    response_in = np.zeros((ntemp, nwl), dtype=np.float64)
    reserr_in = np.zeros(nwl, dtype=np.float64)

    for iwl in range(nwl):
        indwl = np.argmin(np.abs(wlall - wavel[iwl]))
        response_in[:, iwl] = resp_all[indtemp, indwl]
        if ncomp > 0:
            reserr_in[iwl] = (
                np.sum(resp_all[nindtemp, indwl] * dt0[nindtemp]) /
                np.sum(resp_all[indtemp, indwl] * dt0[indtemp])
            )

    # Fixed response uncertainties per channel (Boerner et al. / Morgan 2019)
    wl0 = np.array([94, 131, 171, 193, 211, 304, 335])
    ru0 = np.array([0.5, 0.5, 0.25, 0.25, 0.25, 0.5, 0.25])

    resuncert = np.zeros(nwl, dtype=np.float64)
    for i in range(nwl):
        ind = np.where(wavel[i] == wl0)[0]
        if len(ind) > 0:
            resuncert[i] = ru0[ind[0]]
        else:
            resuncert[i] = 0.5  # fallback for non-standard channels

    reserr = np.sqrt(resuncert ** 2 + reserr_in ** 2)

    # Interpolate to required temperature bins
    if reglog:
        logte_out = np.linspace(logte_in.min(), logte_in.max(), nout)
    else:
        temp_lin = np.linspace(10.0 ** logte_in.min(),
                               10.0 ** logte_in.max(), nout)
        logte_out = np.log10(temp_lin)

    # Temperature bin widths (derivative of 10^logte w.r.t. index)
    dt = np.gradient(10.0 ** logte_in)
    dt2 = np.gradient(10.0 ** logte_out)

    # Spline interpolation of response / dt → multiply by dt2
    response_out = np.zeros((nout, nwl), dtype=np.float64)
    for i in range(nwl):
        f_interp = interp1d(logte_in, response_in[:, i] / dt,
                            kind='cubic', fill_value='extrapolate')
        response_out[:, i] = f_interp(logte_out) * dt2

    dtemp = dt2

    return {
        'logte_out': logte_out,
        'response_out': response_out,
        'reserr': reserr,
        'dtemp': dtemp,
    }
