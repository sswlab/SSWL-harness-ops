"""
SITES DEM inversion for a single spatial pixel.

Given multi-channel measurements, associated uncertainties, temperature
response curves, response relative uncertainties, and temperature bin widths,
this implements the SITES inversion described in Morgan (2019).

Reference:
    Morgan, H. 2019, Sol Phys, 294, 135
    https://ui.adsabs.harvard.edu/abs/2019SoPh..294..135M/abstract
"""

import numpy as np
from scipy.ndimage import convolve1d


def _gaussian_kernel(sigma):
    """Create a normalized Gaussian kernel matching IDL gaussian_function(/NORM).

    Parameters
    ----------
    sigma : float
        Standard deviation of the Gaussian (in array-index units).

    Returns
    -------
    ker : ndarray
        1-D normalized Gaussian kernel (sums to 1).
    """
    width = int(np.ceil(3.0 * sigma)) * 2 + 1
    x = np.arange(width) - width // 2
    ker = np.exp(-0.5 * (x / sigma) ** 2)
    ker = ker / ker.sum()
    return ker


def dem_sites(obs_in, err_in, response, response_err, delta_temp,
              convergence=1.0e-2, ker=None, res2=None, totres2=None):
    """SITES DEM inversion for a single pixel.

    Parameters
    ----------
    obs_in : array_like, shape (nwl,)
        Multi-channel measurement (e.g. 6-element AIA DN/s vector).
    err_in : array_like, shape (nwl,)
        Absolute measurement uncertainties, same units as obs_in.
    response : array_like, shape (nt, nwl)
        Temperature response functions for each channel.
    response_err : array_like, shape (nwl,)
        Relative (fractional) uncertainties of the response functions.
    delta_temp : array_like, shape (nt,)
        Width of each temperature bin in Kelvin.
    convergence : float, optional
        Convergence threshold. Default 1e-2 (1%).
    ker : array_like or None, optional
        Smoothing kernel. If None, a default Gaussian kernel is used.
    res2 : ndarray or None, optional
        Pre-computed response * delta_temp array for efficiency when
        processing many pixels. Returned in output for reuse.
    totres2 : ndarray or None, optional
        Pre-computed sum of res2**2 along temperature axis. Returned
        in output for reuse.

    Returns
    -------
    dict with keys:
        'dem'      : ndarray, shape (nt,) — DEM at each temperature bin
        'obsmod'   : ndarray, shape (nwl,) — model measurement
        'demerr'   : ndarray, shape (nt,) — absolute DEM errors
        'irep'     : int — number of iterations
        'gres'     : ndarray, shape (nt, nwl) — weighted relative responses
        'res2'     : ndarray, shape (nt, nwl) — response * delta_temp
        'totres2'  : ndarray, shape (nwl,) — total(res2^2, axis=0)
        'ker'      : ndarray — smoothing kernel used
    """
    obs_in = np.asarray(obs_in, dtype=np.float64)
    err_in = np.asarray(err_in, dtype=np.float64)
    response = np.asarray(response, dtype=np.float64)
    response_err = np.asarray(response_err, dtype=np.float64)
    delta_temp = np.asarray(delta_temp, dtype=np.float64)

    nt, nwl = response.shape

    # --- Weights (eq. 2 of Morgan 2019) ---
    wt = 1.0 / np.sqrt((err_in / obs_in) ** 2 + response_err ** 2)  # (nwl,)

    # wwt: broadcast wt to (nt, nwl)
    wwt = wt[np.newaxis, :]  # (1, nwl) → broadcasts to (nt, nwl)

    # gres: weighted relative responses (nt, nwl)
    resp_wwt = response * wwt
    gres = resp_wwt / np.sum(resp_wwt, axis=1, keepdims=True)

    obs = obs_in.copy()

    # --- Smoothing kernel ---
    nker = max(0.08 * nt, 0.5)
    if ker is None:
        ker = _gaussian_kernel(nker)
    else:
        ker = np.asarray(ker, dtype=np.float64)

    # --- Pre-compute res2, totres2 ---
    if res2 is None:
        res2 = response * delta_temp[:, np.newaxis]  # (nt, nwl)
    if totres2 is None:
        totres2 = np.sum(res2 ** 2, axis=0)  # (nwl,)

    res3 = res2 * gres  # (nt, nwl)

    # --- DEM error estimate ---
    demerr_weight = ((err_in / obs_in) ** 2 + response_err ** 2)[np.newaxis, :] * gres
    demerr = np.sqrt(np.sum(demerr_weight, axis=1))  # (nt,)

    # --- Iterative inversion ---
    totwt = np.sum(wt)
    obswt = wt / obs_in  # (nwl,)
    demmain = np.zeros(nt, dtype=np.float64)
    irep = 0

    while True:
        # dem estimate for this iteration
        dem = (obs / totres2)[np.newaxis, :] * res3  # (nt, nwl)

        # accumulate and smooth
        smoothed = convolve1d(np.sum(dem, axis=1), ker,
                              mode='constant', cval=0.0)
        demmain = np.maximum(demmain + smoothed, 0.0)

        # residual observations
        obs = obs_in - np.sum(demmain[:, np.newaxis] * res2, axis=0)

        convobs = np.sum(np.abs(obs * obswt)) / totwt
        irep += 1

        if irep > 300 or convobs < convergence:
            break

    # --- Optional outputs ---
    obsmod = np.sum((demmain * delta_temp)[:, np.newaxis] * response, axis=0)
    demerr = demerr * demmain

    return {
        'dem': demmain,
        'obsmod': obsmod,
        'demerr': demerr,
        'irep': irep,
        'gres': gres,
        'res2': res2,
        'totres2': totres2,
        'ker': ker,
    }
