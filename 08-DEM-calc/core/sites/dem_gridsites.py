"""
Grid-SITES DEM inversion for multiple pixels.

Implements the Grid-SITES wrapper that groups similar multi-channel
measurements into bins and computes DEMs only for unique bin combinations,
mapping results back to all pixels for greatly increased efficiency.

Reference:
    Pickering, J. & Morgan, H. 2019, Sol Phys, 294, 136
    https://ui.adsabs.harvard.edu/abs/2019SoPh..294..136P/abstract
    Morgan, H. 2019, Sol Phys, 294, 135
    https://ui.adsabs.harvard.edu/abs/2019SoPh..294..135M/abstract
"""

import numpy as np
import time

from .robust_min import robust_min
from .dem_sites import dem_sites


def dem_gridsites(obs_in, err_in, response, response_err, logt, delta_temp,
                  wavel, convergence=1.0e-2, grid=None):
    """Grid-SITES DEM inversion for multiple pixels.

    Parameters
    ----------
    obs_in : array_like, shape (npix, nwl)
        Multi-pixel, multi-channel measurements in DN/s.
    err_in : array_like, shape (npix, nwl)
        Absolute measurement uncertainties, same shape as obs_in.
    response : array_like, shape (nt, nwl)
        Temperature response functions for each channel.
    response_err : array_like, shape (nwl,)
        Relative (fractional) response uncertainties.
    logt : array_like, shape (nt,)
        Log10(T) values for each temperature bin.
    delta_temp : array_like, shape (nt,)
        Width of each temperature bin in Kelvin.
    wavel : array_like, shape (nwl,)
        Wavelengths of each channel, e.g. [94, 131, 171, 193, 211, 335].
    convergence : float, optional
        Convergence threshold for SITES inversion. Default 1e-2.
    grid : dict or None, optional
        Existing grid structure from a previous call for incremental
        processing (time series). If None, grid is created from scratch.

    Returns
    -------
    dict with keys:
        'dem'          : ndarray, shape (npix, nt) — DEM at each pixel
        'demerr'       : ndarray, shape (npix, nt) — DEM errors
        'obsmod'       : ndarray, shape (npix, nwl) — model measurements
        'goodoffit'    : ndarray, shape (npix,) — goodness of fit per pixel
        'grid'         : dict — Grid-SITES structure for reuse
        'nprocess'     : int — number of DEMs actually computed
    """
    obs_in = np.asarray(obs_in, dtype=np.float64)
    err_in = np.asarray(err_in, dtype=np.float64)
    response = np.asarray(response, dtype=np.float64)
    response_err = np.asarray(response_err, dtype=np.float64)
    logt = np.asarray(logt, dtype=np.float64)
    delta_temp = np.asarray(delta_temp, dtype=np.float64)
    wavel = np.asarray(wavel)

    npix, nwl = obs_in.shape
    nt = response.shape[0]

    # Work in log10 intensities
    m = np.log10(obs_in)

    # --- Grid parameters ---
    if grid is None:
        print('Calculating GRID-SITES parameters')
        mn = np.zeros(nwl, dtype=np.float64)
        mx = np.zeros(nwl, dtype=np.float64)
        md = np.zeros(nwl, dtype=np.float64)

        for iwl in range(nwl):
            result = robust_min(m[:, iwl], per=0.02)
            mn[iwl] = result['min']
            mx[iwl] = result['max']
            md[iwl] = np.median(m[:, iwl])

        mxbin = 40
        mnbin = 30
        md_range = md.max() - md.min()
        if md_range > 0:
            nbin = np.round(
                mnbin + (md - md.min()) * (mxbin - mnbin) / md_range
            ).astype(np.int64)
        else:
            nbin = np.full(nwl, mnbin, dtype=np.int64)

        dbin = (mx - mn) / nbin
    else:
        print('Reading GRID-SITES parameters from existing grid')
        nbin = grid['nbin'].copy()
        mn = grid['mn'].copy()
        mx = grid['mx'].copy()
        mxbin = int(nbin.max())
        mnbin = int(nbin.min())
        dbin = (mx - mn) / nbin

    # --- Calculate pixel grid indices ---
    print('Calculating pixel grid indices')
    index = np.zeros(npix, dtype=np.uint64)
    mmn = np.zeros((mxbin, nwl), dtype=np.float64)   # mean measurement
    emn = np.zeros((mxbin, nwl), dtype=np.float64)   # mean error
    mst = np.zeros((mxbin, nwl), dtype=np.float64)   # std measurement
    est = np.zeros((mxbin, nwl), dtype=np.float64)   # std error
    indok = np.ones(npix, dtype=np.bool_)

    for iwl in range(nwl - 1, -1, -1):
        ind = np.floor(
            (m[:, iwl] - mn[iwl]) * nbin[iwl] / (mx[iwl] - mn[iwl])
        ).astype(np.int64)

        # Pixels outside bin range
        indok = indok & (ind >= 0) & (ind <= nbin[iwl] - 1)

        for ibin in range(nbin[iwl]):
            ind2 = np.where(ind == ibin)[0]
            if len(ind2) == 0:
                continue
            emn[ibin, iwl] = np.mean(err_in[ind2, iwl])
            mmn[ibin, iwl] = np.mean(obs_in[ind2, iwl])
            if len(ind2) > 1:
                est[ibin, iwl] = np.std(err_in[ind2, iwl], ddof=1)
                mst[ibin, iwl] = np.std(obs_in[ind2, iwl], ddof=1)

        index = (index * np.uint64(nbin[iwl]) + ind.astype(np.uint64)) * indok.astype(np.uint64)

    # Pixels inside/outside grid
    indin = np.where(indok)[0]
    indout = np.where(~indok)[0]
    nout = len(indout)
    print(f'{nout} pixels outside of grid (will be processed individually)')

    # --- Find unique bin combinations ---
    if grid is not None:
        sorted_idx = np.argsort(index[indin])
        indexuniq_all = index[indin][sorted_idx]
        indexuniq_all = indexuniq_all[
            np.concatenate(([True], indexuniq_all[1:] != indexuniq_all[:-1]))
        ]

        # Filter out indices already in grid
        existing = set(grid['index'].tolist())
        indexuniq = np.array(
            [idx for idx in indexuniq_all if idx not in existing],
            dtype=np.uint64
        )
        cntnew = len(indexuniq)
    else:
        sorted_idx = np.argsort(index[indin])
        indexuniq = index[indin][sorted_idx]
        indexuniq = indexuniq[
            np.concatenate(([True], indexuniq[1:] != indexuniq[:-1]))
        ]
        cntnew = len(indexuniq)

    # --- Compute DEMs for unique bins ---
    if cntnew > 0:
        ndem = len(indexuniq)

        # Convert 1D index → per-channel bin indices
        multi_indices = np.unravel_index(indexuniq, tuple(nbin), order='F')
        # multi_indices[iwl] gives bin indices for channel iwl

        griddem = np.zeros((ndem, nt), dtype=np.float64)
        griddemerr = np.zeros((ndem, nt), dtype=np.float64)
        gridobsmod = np.zeros((ndem, nwl), dtype=np.float64)
        gridgof = np.zeros(ndem, dtype=np.float64)

        print(f'Calculating {ndem} DEMs for grid points')

        # Cache for reuse across iterations
        ker_cache = None
        res2_cache = None
        totres2_cache = None

        for idem in range(ndem):
            if idem % 2000 == 0:
                print(f'{idem} out of {ndem - 1}')

            # Extract bin indices for each channel
            indgrid = np.array([multi_indices[iwl][idem]
                                for iwl in range(nwl)])

            # Channel intensities and errors for this bin
            mnow = mmn[indgrid, np.arange(nwl)]
            snow = mst[indgrid, np.arange(nwl)]
            enow = emn[indgrid, np.arange(nwl)]

            # DEM inversion
            result = dem_sites(
                mnow, enow, response, response_err, delta_temp,
                convergence=convergence,
                ker=ker_cache, res2=res2_cache, totres2=totres2_cache
            )
            dem = result['dem']
            demerr = result['demerr']
            obsmod = result['obsmod']
            gres = result['gres']
            ker_cache = result['ker']
            res2_cache = result['res2']
            totres2_cache = result['totres2']

            # Additional error from intensity variance within bin
            gerr = snow / mnow
            demgerr = np.sqrt(
                np.sum((gerr ** 2)[np.newaxis, :] * gres, axis=1)
            )
            demerr = np.sqrt(demgerr ** 2 + demerr ** 2) * dem

            griddem[idem, :] = dem
            griddemerr[idem, :] = demerr
            gridobsmod[idem, :] = obsmod
            gridgof[idem] = (
                np.sqrt(np.sum(((mnow - obsmod) ** 2) / enow ** 2)) / nwl
            )
    else:
        ndem = 0
        griddem = np.zeros((0, nt), dtype=np.float64)
        griddemerr = np.zeros((0, nt), dtype=np.float64)
        gridobsmod = np.zeros((0, nwl), dtype=np.float64)
        gridgof = np.zeros(0, dtype=np.float64)

    # --- Build / update grid structure ---
    if grid is None:
        grid = {
            'nbin': nbin,
            'logt': logt,
            'wl': wavel,
            'mn': mn,
            'mx': mx,
            'index': indexuniq,
            'dem': griddem,
            'demerr': griddemerr,
            'obsmod': gridobsmod,
            'gof': gridgof,
            'cntdata': np.zeros(ndem, dtype=np.int64),
        }
    else:
        if cntnew > 0:
            grid['index'] = np.concatenate([grid['index'], indexuniq])
            grid['dem'] = np.concatenate([grid['dem'], griddem], axis=0)
            grid['demerr'] = np.concatenate([grid['demerr'], griddemerr], axis=0)
            grid['obsmod'] = np.concatenate([grid['obsmod'], gridobsmod], axis=0)
            grid['gof'] = np.concatenate([grid['gof'], gridgof])
            grid['cntdata'] = np.concatenate([
                grid['cntdata'], np.zeros(ndem, dtype=np.int64)
            ])

    # --- Map grid results back to pixels ---
    print('Mapping GRID-SITES DEMs into output result')
    st = time.time()

    # Build reverse lookup: grid index value → position in grid arrays
    grid_lookup = {}
    for i, gidx in enumerate(grid['index']):
        grid_lookup[int(gidx)] = i

    dataind = []
    demind = []
    for ipix in range(npix):
        key = int(index[ipix])
        if key in grid_lookup:
            dataind.append(ipix)
            demind.append(grid_lookup[key])

    dataind = np.array(dataind, dtype=np.int64)
    demind = np.array(demind, dtype=np.int64)

    demmain = np.zeros((npix, nt), dtype=np.float64)
    demerrmain = np.zeros((npix, nt), dtype=np.float64)
    obsmodmain = np.zeros((npix, nwl), dtype=np.float64)
    goodoffit_main = np.zeros(npix, dtype=np.float64)

    if len(dataind) > 0:
        demmain[dataind, :] = grid['dem'][demind, :]
        demerrmain[dataind, :] = grid['demerr'][demind, :]
        obsmodmain[dataind, :] = grid['obsmod'][demind, :]
        goodoffit_main[dataind] = (
            np.sqrt(np.sum(
                ((obs_in[dataind, :] - grid['obsmod'][demind, :]) ** 2) /
                (err_in[dataind, :] ** 2), axis=1
            )) / nwl
        )

    print(f'Mapping time = {time.time() - st:.3f} s')

    # --- Process pixels outside grid individually ---
    if nout > 0:
        print(f'Calculating DEM for {nout} non-gridded pixels')

        ker_cache2 = None
        res2_cache2 = None
        totres2_cache2 = None

        for idem in range(nout):
            if idem % 2000 == 0:
                print(f'{idem} out of {nout - 1}')

            inddata = indout[idem]
            mnow = obs_in[inddata, :]
            enow = err_in[inddata, :]

            result = dem_sites(
                mnow, enow, response, response_err, delta_temp,
                convergence=convergence,
                ker=ker_cache2, res2=res2_cache2, totres2=totres2_cache2
            )
            ker_cache2 = result['ker']
            res2_cache2 = result['res2']
            totres2_cache2 = result['totres2']

            demmain[inddata, :] = result['dem']
            demerrmain[inddata, :] = result['demerr']
            obsmodmain[inddata, :] = result['obsmod']
            goodoffit_main[inddata] = (
                np.sqrt(np.sum(
                    ((mnow - result['obsmod']) ** 2) / enow ** 2
                )) / nwl
            )

    nprocess = nout + cntnew

    return {
        'dem': demmain,
        'demerr': demerrmain,
        'obsmod': obsmodmain,
        'goodoffit': goodoffit_main,
        'grid': grid,
        'nprocess': nprocess,
    }
