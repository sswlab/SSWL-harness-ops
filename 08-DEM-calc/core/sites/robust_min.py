"""
Robust minimum/maximum of an array.

Calculates the robust minimum (and optionally maximum) of an input array
by sorting and interpolating to a given percentile.

Reference:
    Huw Morgan, Aberystwyth University, 2019
    STFC Consolidated grant to Aberystwyth University (Morgan)
"""

import numpy as np


def robust_min(y0, per=1.0):
    """Calculate the robust minimum (and maximum) of an array.

    Sorts finite array members into ascending order, then interpolates
    to the value where the number of array members equals the percentile.

    Parameters
    ----------
    y0 : array_like
        Input numerical array.
    per : float, optional
        The percentile minimum to use. Default is 1%.

    Returns
    -------
    dict
        'min' : float — robust minimum value (NaN if no finite values)
        'max' : float — robust maximum value at the same percentile
    """
    y0 = np.asarray(y0, dtype=np.float64)

    indok = np.where(np.isfinite(y0))[0]
    n = len(indok)
    if n == 0:
        return {'min': np.nan, 'max': np.nan}

    indsort = np.argsort(y0[indok])
    sorted_vals = y0[indok[indsort]]

    indmin = per * float(n - 1) / 100.0
    indmax = (100.0 - per) * float(n - 1) / 100.0

    rmin = np.interp(indmin, np.arange(n, dtype=np.float64), sorted_vals)
    rmax = np.interp(indmax, np.arange(n, dtype=np.float64), sorted_vals)

    return {'min': float(rmin), 'max': float(rmax)}
