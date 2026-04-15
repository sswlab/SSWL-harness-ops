"""
Read AIA files and return datacube with noise estimates.

Reads AIA FITS files (synoptic or full-resolution) and returns a datacube
of [ny, nx, nchannels] in DN/s units, along with Poisson + measurement
noise estimates based on Boerner et al. (2012, Sol Phys, 275, 41).

Replaces the IDL SSW dependencies (read_sdo, aia_prep, AIA_BP_READ_ERROR_TABLE,
fitshead2wcs, wcs_get_coord, pb0r, anytim2tai, anytim2cal, one2n) with
SunPy, Astropy, and aiapy equivalents.

Reference:
    Morgan, H. 2019, Sol Phys, 294, 135
    Boerner, P. et al. 2012, Sol Phys, 275, 41
"""

import numpy as np
from astropy.io import fits
from astropy.time import Time
from scipy.ndimage import median_filter

try:
    import sunpy.map
    HAS_SUNPY = True
except ImportError:
    HAS_SUNPY = False

try:
    from sunpy.coordinates.sun import angular_radius as _sun_angular_radius
    HAS_SUNPY_COORDS = True
except ImportError:
    HAS_SUNPY_COORDS = False

try:
    import aiapy.calibrate
    HAS_AIAPY = True
except ImportError:
    HAS_AIAPY = False


# ── Boerner et al. (2012) error table ──────────────────────────────────
# Replaces IDL AIA_BP_READ_ERROR_TABLE()
_AIA_ERROR_TABLE = {
    94:  {'dnperpht': 2.128, 'compress': 0.0},
    131: {'dnperpht': 1.523, 'compress': 0.0},
    171: {'dnperpht': 1.168, 'compress': 0.7},
    193: {'dnperpht': 1.024, 'compress': 0.7},
    211: {'dnperpht': 0.946, 'compress': 0.7},
    304: {'dnperpht': 0.658, 'compress': 0.7},
    335: {'dnperpht': 0.596, 'compress': 0.0},
}


def _rebin_2d(arr, ny_new, nx_new):
    """Block-average a 2-D array to a new shape (IDL REBIN equivalent)."""
    ny_old, nx_old = arr.shape
    by = ny_old // ny_new
    bx = nx_old // nx_new
    return arr.reshape(ny_new, by, nx_new, bx).mean(axis=(1, 3))


def _solar_radius_arcsec(date_obs):
    """Get apparent solar radius in arcsec (replaces IDL pb0r)."""
    if HAS_SUNPY_COORDS:
        import astropy.units as u
        return _sun_angular_radius(Time(date_obs)).to(u.arcsec).value

    # Fallback: approximate from mean value
    return 959.63  # mean angular radius in arcsec


def dem_openaiafiles_sites(files, npixuser=1024, clip=None,
                            synoptic=False, maxht=1.15, clean=False):
    """Read AIA files and produce a datacube with noise estimates.

    Parameters
    ----------
    files : list
        Either:
        (i) list of N filenames, one per channel, or
        (ii) list of N lists, each containing one or more filenames
             for a channel (multiple exposures are averaged).
    npixuser : int, optional
        Required full-image size. E.g. 1024 → rebin 4096×4096 to
        1024×1024. Must be an integer factor of the AIA image size.
        Default 1024.
    clip : list of 4 ints or None, optional
        Sub-region [xleft, ybottom, xright, ytop] in pixels (applied
        after rebinning). Default None (full image).
    synoptic : bool, optional
        If True, files are AIA synoptic data (already calibrated).
        If False (default), full-resolution files are calibrated via
        aiapy if available.
    maxht : float, optional
        Maximum heliocentric distance in solar radii. Pixels beyond
        this are set to NaN. Default 1.15.
    clean : bool, optional
        If True, replace zero/negative pixels with local medians.
        Effective but slow. Default False.

    Returns
    -------
    dict with keys:
        'out'            : ndarray, shape (ny, nx, nwl) — datacube [DN/s]
        'hdrmain'        : list of FITS headers per channel
        'hdrsave'        : dict — master header for the datacube
        'noise_estimate' : ndarray, shape (ny, nx, nwl) — noise [DN/s]
    """
    nwl = len(files)
    nx = npixuser
    ny = npixuser

    cdeltmain = 0.60000002 * 4096 / nx

    out = None
    noise_estimate = None
    hdrmain = [None] * nwl
    tai_all = np.zeros(nwl, dtype=np.float64)
    cdelt_all = np.zeros(nwl, dtype=np.float64)
    crpix1_all = np.zeros(nwl, dtype=np.float64)
    crpix2_all = np.zeros(nwl, dtype=np.float64)

    last_hdr = None

    for iwl in range(nwl):
        # Handle file input: single filename or list of filenames
        filesnow = files[iwl]
        if isinstance(filesnow, str):
            filesnow = [filesnow]
        nfiles = len(filesnow)

        print(f'Reading in files for channel {iwl} (patience!)')

        # ── Read FITS data ──────────────────────────────────────────
        im_list = []
        hdr_list = []

        for fname in filesnow:
            if HAS_SUNPY and not synoptic and HAS_AIAPY:
                # Full-res: calibrate with aiapy
                smap = sunpy.map.Map(fname)
                smap_updated = aiapy.calibrate.update_pointing(smap)
                smap_reg = aiapy.calibrate.register(smap_updated)
                data = smap_reg.data.astype(np.float32)
                hdr = dict(smap_reg.fits_header)
            elif HAS_SUNPY:
                smap = sunpy.map.Map(fname)
                data = smap.data.astype(np.float32)
                hdr = dict(smap.fits_header)
            else:
                with fits.open(fname) as hdul:
                    data = hdul[1].data.astype(np.float32)
                    hdr = dict(hdul[1].header)

            im_list.append(data)
            hdr_list.append(hdr)

        # Stack images: (nimage, ny_raw, nx_raw)
        im = np.stack(im_list, axis=0)
        nimage = im.shape[0]
        hdr = hdr_list[0]

        # Get exposure times
        exptime = np.array([h.get('EXPTIME', 1.0) for h in hdr_list])

        # ── Dark image check ────────────────────────────────────────
        if hdr.get('IMG_TYPE', '') == 'DARK' or hdr.get('EXPTIME', 1.0) < 0.1:
            print('Dark image, skipping')
            return {
                'out': None, 'hdrmain': None,
                'hdrsave': None, 'noise_estimate': None
            }

        naxis1 = int(hdr.get('NAXIS1', im.shape[2]))
        naxis2 = int(hdr.get('NAXIS2', im.shape[1]))

        # Fix synoptic header if needed
        if naxis1 != 4096:
            hdr['CDELT1'] = 0.60000002 * 4096 / naxis1
            hdr['CDELT2'] = 0.60000002 * 4096 / naxis2

        # ── Saturated pixel handling ────────────────────────────────
        indsat = im >= 1.4e4
        im[indsat] = np.nan

        # ── Clean negative pixels (optional) ────────────────────────
        if clean:
            for i in range(nimage):
                frame = im[i]
                for ksize in [3, 5, 7]:
                    indneg = frame <= 0
                    if not np.any(indneg):
                        break
                    md = median_filter(frame, size=ksize)
                    frame[indneg] = md[indneg]
                im[i] = frame

        # ── Noise estimation (Boerner model) ────────────────────────
        print('Estimating count noise')
        wavelnth = int(hdr.get('WAVELNTH', 171))
        terr = _AIA_ERROR_TABLE.get(wavelnth,
                                     {'dnperpht': 1.0, 'compress': 0.7})

        cdelt1 = float(hdr.get('CDELT1', 0.6))
        cdelt2 = float(hdr.get('CDELT2', 0.6))
        sumfactor = round(cdelt1 / 0.6) * round(cdelt2 / 0.6)

        dnperpht = terr['dnperpht']
        noisenow = np.sqrt(np.abs(im / dnperpht)) * dnperpht  # (nimage, ny, nx)

        # ── Rebin if needed ─────────────────────────────────────────
        if naxis2 != ny or naxis1 != nx:
            print('Rebinning images to required pixel size')
            im_rb = np.zeros((nimage, ny, nx), dtype=np.float32)
            noise_rb = np.zeros((nimage, ny, nx), dtype=np.float32)
            for i in range(nimage):
                im_rb[i] = _rebin_2d(im[i], ny, nx)
                noise_rb[i] = _rebin_2d(noisenow[i], ny, nx)
            im = im_rb
            noisenow = noise_rb

            sumfactor = sumfactor * (naxis1 / float(nx)) * (naxis2 / float(ny))

            # Adjust header
            shrink = float(nx) / naxis1
            hdr['NAXIS1'] = nx
            hdr['NAXIS2'] = ny
            hdr['CDELT1'] = cdelt1 / shrink
            hdr['CDELT2'] = cdelt2 / shrink
            hdr['CRPIX1'] = float(hdr.get('CRPIX1', naxis1 / 2)) * shrink
            hdr['CRPIX2'] = float(hdr.get('CRPIX2', naxis2 / 2)) * shrink

        # ── Off-limb masking ────────────────────────────────────────
        print('Calculating image geometry')
        crpix1 = float(hdr.get('CRPIX1', nx / 2))
        crpix2 = float(hdr.get('CRPIX2', ny / 2))
        cdelt1_now = float(hdr.get('CDELT1', cdeltmain))
        cdelt2_now = float(hdr.get('CDELT2', cdeltmain))

        # Helioprojective coordinates in arcsec (0-based pixel indexing)
        xx = (np.arange(nx) - (crpix1 - 1)) * cdelt1_now
        yy = (np.arange(ny) - (crpix2 - 1)) * cdelt2_now
        xx2d, yy2d = np.meshgrid(xx, yy)  # (ny, nx)
        ht = np.sqrt(xx2d ** 2 + yy2d ** 2)

        date_obs = hdr.get('DATE-OBS', hdr.get('DATE_OBS', '2020-01-01T00:00:00'))
        rsun = _solar_radius_arcsec(date_obs)
        ht = ht / rsun

        mask_offlimb = ht > maxht
        for i in range(nimage):
            im[i][mask_offlimb] = np.nan
            noisenow[i][mask_offlimb] = np.nan

        # ── Clip to sub-region ──────────────────────────────────────
        if clip is not None and len(clip) == 4:
            print('Clipping image')
            xl, yb, xr, yt = clip
            im = im[:, yb:yt + 1, xl:xr + 1]
            noisenow = noisenow[:, yb:yt + 1, xl:xr + 1]

        # ── Uncertainty estimation ──────────────────────────────────
        print('Estimating uncertainties')
        sumfactor_total = sumfactor * nimage
        noisenow = noisenow / np.sqrt(sumfactor_total)

        darknoise = 0.18
        readnoise = 1.15 / np.sqrt(sumfactor_total)
        quantnoise = 0.288819 / np.sqrt(sumfactor_total)

        compressratio = terr['compress']
        if compressratio > 0:
            compressnoise = np.maximum(noisenow / compressratio, 0.288819)
        else:
            compressnoise = np.full_like(noisenow, 0.288819)

        lowcounts = im < 25
        compressnoise[lowcounts] = 0.0
        compressnoise = compressnoise / np.sqrt(sumfactor_total)

        noisenow = np.sqrt(
            noisenow ** 2 + darknoise ** 2 + readnoise ** 2 +
            quantnoise ** 2 + compressnoise ** 2
        )

        # ── Normalize by exposure time ──────────────────────────────
        print('Normalizing by exposure time')
        for i in range(nimage):
            im[i] = im[i] / exptime[i]
            noisenow[i] = noisenow[i] / exptime[i]

        # ── Combine multiple exposures ──────────────────────────────
        if nimage > 1:
            print(f'Combining {nimage} images')
            masknan = np.sum(~np.isfinite(im), axis=0) > 0
            im_combined = np.nanmean(im, axis=0)
            noise_combined = np.nanmean(noisenow, axis=0)
            im_combined[masknan] = np.nan
            noise_combined[masknan] = np.nan
        else:
            im_combined = im[0]
            noise_combined = noisenow[0]

        hdr['EXPTIME'] = 1.0

        # ── Initialize output cube on first channel ─────────────────
        if out is None:
            nyout, nxout = im_combined.shape
            out = np.zeros((nyout, nxout, nwl), dtype=np.float32)
            noise_estimate = np.zeros((nyout, nxout, nwl), dtype=np.float32)

        out[:, :, iwl] = im_combined
        noise_estimate[:, :, iwl] = noise_combined
        hdrmain[iwl] = hdr

        tai_all[iwl] = Time(date_obs).tai.unix_tai
        cdelt_all[iwl] = cdeltmain

        if clip is not None and len(clip) == 4:
            crpix1_all[iwl] = float(hdr.get('CRPIX1', nx / 2)) - clip[0]
            crpix2_all[iwl] = float(hdr.get('CRPIX2', ny / 2)) - clip[1]

        last_hdr = hdr

    # ── Master header ───────────────────────────────────────────────
    print('Adjusting header')
    hdrsave = dict(last_hdr) if last_hdr is not None else {}
    if out is not None:
        hdrsave['NAXIS1'] = out.shape[1]
        hdrsave['NAXIS2'] = out.shape[0]
    hdrsave['WAVELNTH'] = 0
    hdrsave['WAVE_STR'] = 'tempmap'

    mean_tai = np.mean(tai_all)
    hdrsave['DATE-OBS'] = Time(mean_tai, format='unix_tai',
                               scale='tai').utc.isot
    hdrsave['CDELT1'] = float(np.median(cdelt_all))
    hdrsave['CDELT2'] = float(np.median(cdelt_all))
    if clip is not None:
        hdrsave['CRPIX1'] = float(np.median(crpix1_all))
        hdrsave['CRPIX2'] = float(np.median(crpix2_all))

    return {
        'out': out,
        'hdrmain': hdrmain,
        'hdrsave': hdrsave,
        'noise_estimate': noise_estimate,
    }
