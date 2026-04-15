"""
Multi-format data loader for DEM harness.

Supports:
  (1) Individual .npy files  — filename must contain wavelength (e.g. aia_94.npy)
  (2) Single .npz file       — keys are wavelength strings ('94','131',...)
  (3) Individual .fits files  — WAVELNTH header or filename wavelength
  (4) Response functions      — .npy, .npz, or bundled AIA/EUI fallback

Instruments:
  - AIA: 94, 131, 171, 193, 211, 335 Å
  - EUI: 94, 131, 174, 193, 211, 335 Å  (FSI 174 replaces AIA 171)

Wavelength extraction: regex searches for known wavelengths in filename.
"""

import os
import re
import glob
import numpy as np

# Standard wavelengths per instrument
AIA_WAVELENGTHS = [94, 131, 171, 193, 211, 335]
EUI_WAVELENGTHS = [94, 131, 174, 193, 211, 335]
ALL_KNOWN_WAVELENGTHS = sorted(set(AIA_WAVELENGTHS + EUI_WAVELENGTHS))

# Regex: match known wavelength numbers
_WL_PATTERN = re.compile(
    r'(?:^|[_\-./\\])(' + '|'.join(str(w) for w in ALL_KNOWN_WAVELENGTHS) + r')(?:[_\-./\\]|\.|\b)'
)


def _extract_wavelength(filename):
    """Extract AIA wavelength from a filename.

    Examples
    --------
    >>> _extract_wavelength('aia_94.npy')
    94
    >>> _extract_wavelength('/data/obs_131_lev1.fits')
    131
    >>> _extract_wavelength('image_335.npy')
    335
    """
    basename = os.path.basename(filename)
    match = _WL_PATTERN.search(basename)
    if match:
        return int(match.group(1))
    # Fallback: search for any AIA wavelength as standalone number
    for wl in AIA_WAVELENGTHS:
        if re.search(rf'\b{wl}\b', basename):
            return wl
    return None


def _load_fits_image(filepath):
    """Load a single FITS file, return (data_dns, header).

    Attempts to normalize to DN/s using EXPTIME from header.
    """
    from astropy.io import fits as pyfits

    with pyfits.open(filepath) as hdul:
        # AIA: data in primary or 1st extension
        if hdul[0].data is not None and hdul[0].data.ndim == 2:
            data = hdul[0].data.astype(np.float64)
            header = dict(hdul[0].header)
        elif len(hdul) > 1 and hdul[1].data is not None:
            data = hdul[1].data.astype(np.float64)
            header = dict(hdul[1].header)
        else:
            raise ValueError(f"No 2D image data found in {filepath}")

    # Normalize to DN/s
    exptime = float(header.get('EXPTIME', 1.0))
    if exptime > 0 and exptime != 1.0:
        data = data / exptime
        header['EXPTIME'] = 1.0

    return data, header


def _estimate_aia_error(data_dns, header):
    """Estimate DN error using Boerner et al. (2012) noise model.

    Parameters
    ----------
    data_dns : ndarray
        Image in DN/s (already exposure-normalized).
    header : dict
        FITS header (needs WAVELNTH).

    Returns
    -------
    error : ndarray
        Error estimate in DN/s.
    """
    # Boerner et al. (2012) parameters per channel
    # EUI 174Å: gain=31.025, rdnse=2.0, dn2ph denom=1696 (from DEM_2024_11 notebooks)
    error_table = {
        94:  {'dnperpht': 2.128, 'readnoise': 1.14},
        131: {'dnperpht': 1.523, 'readnoise': 1.18},
        171: {'dnperpht': 1.168, 'readnoise': 1.15},
        174: {'dnperpht': 3.182, 'readnoise': 2.00},  # EUI FSI 174: gain=31.025*174/1696
        193: {'dnperpht': 1.024, 'readnoise': 1.20},
        211: {'dnperpht': 0.946, 'readnoise': 1.20},
        335: {'dnperpht': 0.596, 'readnoise': 1.18},
    }

    wl = int(header.get('WAVELNTH', 171))
    params = error_table.get(wl, {'dnperpht': 1.0, 'readnoise': 1.15})

    # Poisson + read noise (in DN/s, assuming exptime=1)
    shot = np.sqrt(np.abs(data_dns) * params['dnperpht']) * params['dnperpht']
    error = np.sqrt(shot**2 + params['readnoise']**2)

    # Minimum error floor to avoid division by zero in DEM inversion
    error = np.maximum(error, 0.01)

    return error


def detect_instrument(wavelengths):
    """Determine instrument from wavelength list.

    Returns 'AIA', 'EUI', or 'mixed'.
    """
    wl_set = set(wavelengths)
    if 174 in wl_set and 171 not in wl_set:
        return 'EUI'
    if 171 in wl_set and 174 not in wl_set:
        return 'AIA'
    if 174 in wl_set and 171 in wl_set:
        return 'mixed'
    return 'AIA'  # default


def _detect_wavelengths(data_dir):
    """Auto-detect wavelengths from files in directory.

    Scans filenames for known wavelengths to determine AIA vs EUI.
    """
    all_files = (
        glob.glob(os.path.join(data_dir, '*.npy')) +
        glob.glob(os.path.join(data_dir, '*.npz')) +
        glob.glob(os.path.join(data_dir, '*.fits')) +
        glob.glob(os.path.join(data_dir, '*.fts')) +
        glob.glob(os.path.join(data_dir, '*.fit'))
    )

    found_wl = set()
    for fpath in all_files:
        wl = _extract_wavelength(fpath)
        if wl is not None:
            found_wl.add(wl)

    # Also check npz keys
    for fpath in glob.glob(os.path.join(data_dir, '*.npz')):
        try:
            data = np.load(fpath)
            for key in data.keys():
                try:
                    val = int(key)
                    if val in ALL_KNOWN_WAVELENGTHS:
                        found_wl.add(val)
                except ValueError:
                    wl = _extract_wavelength(key + '.npz')
                    if wl is not None:
                        found_wl.add(wl)
        except Exception:
            pass

    if 174 in found_wl:
        result = EUI_WAVELENGTHS
        print(f"[loader] EUI 파장 감지 (174Å): {result}")
    elif 171 in found_wl:
        result = AIA_WAVELENGTHS
        print(f"[loader] AIA 파장 감지 (171Å): {result}")
    else:
        result = AIA_WAVELENGTHS
        print(f"[loader] 파장 감지 실패, AIA 기본값 사용: {result}")

    return result


def load_data(data_dir, wavelengths=None):
    """Auto-detect and load 6-channel data from a directory.

    Supported layouts
    -----------------
    1. Individual .npy files with wavelength in filename
    2. Single .npz with wavelength keys ('94', '131', ...)
    3. Individual .fits files with wavelength in filename or WAVELNTH header

    Parameters
    ----------
    data_dir : str
        Directory containing the data files.
    wavelengths : list of int or None
        Wavelengths to load. Default: [94, 131, 171, 193, 211, 335].

    Returns
    -------
    dict with keys:
        'dn_cube'     : ndarray, shape (ny, nx, nwl) — DN/s
        'edn_cube'    : ndarray, shape (ny, nx, nwl) — error estimate
        'wavelengths' : list of int — channel wavelengths in order
        'headers'     : list of dict or None — FITS headers (if FITS input)
        'format'      : str — detected format ('npy', 'npz', 'fits')
        'files'       : dict — {wavelength: filepath} mapping
    """
    if wavelengths is None:
        raise ValueError(
            "wavelengths must be specified explicitly.\n"
            "예: wavelengths=[94,131,171,193,211,335] (AIA)\n"
            "    wavelengths=[94,131,174,193,211,335] (EUI-FSI)\n"
            "사용자에게 기기/파장을 먼저 확인하세요."
        )

    nwl = len(wavelengths)

    # --- Detect format ---
    npy_files = sorted(glob.glob(os.path.join(data_dir, '*.npy')))
    npz_files = sorted(glob.glob(os.path.join(data_dir, '*.npz')))
    fits_files = sorted(
        glob.glob(os.path.join(data_dir, '*.fits')) +
        glob.glob(os.path.join(data_dir, '*.fts')) +
        glob.glob(os.path.join(data_dir, '*.fit'))
    )

    # Try npz first (single file, explicit keys)
    if npz_files:
        return _load_npz(npz_files, wavelengths)

    # Then npy (individual files)
    if npy_files:
        return _load_npy(npy_files, wavelengths)

    # Then FITS
    if fits_files:
        return _load_fits(fits_files, wavelengths)

    raise FileNotFoundError(
        f"No .npy, .npz, or .fits files found in {data_dir}\n"
        f"Expected: individual files with wavelength in filename "
        f"(e.g. aia_94.npy) or a single .npz with wavelength keys."
    )


def _load_npz(npz_files, wavelengths):
    """Load from .npz file(s).

    Tries each .npz file for wavelength keys.
    Keys can be: '94', '131', ... or 'aia_94', 'data_131', etc.
    Also accepts key 'dn_cube' with shape (ny, nx, nwl).
    """
    for npz_path in npz_files:
        data = np.load(npz_path)
        keys = list(data.keys())

        # Case 1: keys are wavelength strings
        wl_map = {}
        for key in keys:
            wl = _extract_wavelength(key + '.npz')
            if wl is None:
                # Try direct int parse
                try:
                    val = int(key)
                    if val in wavelengths:
                        wl = val
                except ValueError:
                    pass
            if wl is not None and wl in wavelengths:
                wl_map[wl] = key

        if len(wl_map) >= len(wavelengths):
            # All wavelengths found
            first_key = wl_map[wavelengths[0]]
            ny, nx = data[first_key].shape
            dn_cube = np.zeros((ny, nx, len(wavelengths)), dtype=np.float64)
            for i, wl in enumerate(wavelengths):
                dn_cube[:, :, i] = data[wl_map[wl]].astype(np.float64)

            # Check for error cube
            edn_cube = None
            for ekey_prefix in ['edn', 'err', 'error', 'noise']:
                err_map = {}
                for key in keys:
                    if key.startswith(ekey_prefix):
                        ewl = _extract_wavelength(key + '.npz')
                        if ewl is None:
                            try:
                                ewl = int(key.replace(ekey_prefix + '_', '').replace(ekey_prefix, ''))
                            except ValueError:
                                pass
                        if ewl in wavelengths:
                            err_map[ewl] = key
                if len(err_map) >= len(wavelengths):
                    edn_cube = np.zeros((ny, nx, len(wavelengths)), dtype=np.float64)
                    for i, wl in enumerate(wavelengths):
                        edn_cube[:, :, i] = data[err_map[wl]].astype(np.float64)
                    break

            if edn_cube is None:
                # Simple Poisson estimate
                edn_cube = np.maximum(np.sqrt(np.abs(dn_cube)), 0.01)

            # Clean NaN/negative
            dn_cube, edn_cube = _clean_data(dn_cube, edn_cube)

            return {
                'dn_cube': dn_cube,
                'edn_cube': edn_cube,
                'wavelengths': wavelengths,
                'headers': None,
                'format': 'npz',
                'files': {wl: f"{npz_path}[{wl_map[wl]}]" for wl in wavelengths},
            }

        # Case 2: 'dn_cube' key with shape (ny, nx, nwl)
        if 'dn_cube' in keys:
            dn_cube = data['dn_cube'].astype(np.float64)
            edn_cube = data.get('edn_cube', None)
            if edn_cube is not None:
                edn_cube = edn_cube.astype(np.float64)
            else:
                edn_cube = np.maximum(np.sqrt(np.abs(dn_cube)), 0.01)

            dn_cube, edn_cube = _clean_data(dn_cube, edn_cube)

            wl_loaded = data.get('wavelengths', np.array(wavelengths))

            return {
                'dn_cube': dn_cube,
                'edn_cube': edn_cube,
                'wavelengths': list(wl_loaded.astype(int)),
                'headers': None,
                'format': 'npz',
                'files': {int(wl_loaded[i]): npz_path for i in range(len(wl_loaded))},
            }

    raise ValueError(
        f"No matching wavelength keys found in .npz files.\n"
        f"Expected keys: {[str(w) for w in wavelengths]} or 'dn_cube'."
    )


def _load_npy(npy_files, wavelengths):
    """Load from individual .npy files."""
    wl_file_map = {}

    for fpath in npy_files:
        wl = _extract_wavelength(fpath)
        if wl is not None and wl in wavelengths:
            wl_file_map[wl] = fpath

    missing = set(wavelengths) - set(wl_file_map.keys())
    if missing:
        raise FileNotFoundError(
            f"Missing .npy files for wavelengths: {sorted(missing)}\n"
            f"Found: {wl_file_map}\n"
            f"Files need wavelength in filename (e.g. aia_94.npy, data_131.npy)"
        )

    # Load first to get shape
    first = np.load(wl_file_map[wavelengths[0]])
    ny, nx = first.shape[:2]
    nwl = len(wavelengths)

    dn_cube = np.zeros((ny, nx, nwl), dtype=np.float64)
    for i, wl in enumerate(wavelengths):
        arr = np.load(wl_file_map[wl]).astype(np.float64)
        if arr.shape[:2] != (ny, nx):
            raise ValueError(
                f"Shape mismatch: {wl}Å is {arr.shape} but {wavelengths[0]}Å is ({ny},{nx})"
            )
        dn_cube[:, :, i] = arr if arr.ndim == 2 else arr[:, :, 0]

    # Check for corresponding error files
    edn_cube = _try_load_error_npy(os.path.dirname(npy_files[0]), wavelengths, ny, nx)
    if edn_cube is None:
        edn_cube = np.maximum(np.sqrt(np.abs(dn_cube)), 0.01)

    dn_cube, edn_cube = _clean_data(dn_cube, edn_cube)

    return {
        'dn_cube': dn_cube,
        'edn_cube': edn_cube,
        'wavelengths': wavelengths,
        'headers': None,
        'format': 'npy',
        'files': wl_file_map,
    }


def _try_load_error_npy(data_dir, wavelengths, ny, nx):
    """Try to find error .npy files (e.g. err_94.npy, edn_131.npy)."""
    for prefix in ['err', 'edn', 'error', 'noise', 'sigma']:
        all_found = True
        edn_cube = np.zeros((ny, nx, len(wavelengths)), dtype=np.float64)
        for i, wl in enumerate(wavelengths):
            candidates = glob.glob(os.path.join(data_dir, f'{prefix}*{wl}*.npy'))
            if candidates:
                edn_cube[:, :, i] = np.load(candidates[0]).astype(np.float64)
            else:
                all_found = False
                break
        if all_found:
            return edn_cube
    return None


def _load_fits(fits_files, wavelengths):
    """Load from individual FITS files."""
    from astropy.io import fits as pyfits

    wl_file_map = {}

    for fpath in fits_files:
        # Try filename first
        wl = _extract_wavelength(fpath)

        # Fallback: read WAVELNTH from header
        if wl is None:
            try:
                with pyfits.open(fpath) as hdul:
                    hdr = hdul[0].header if hdul[0].data is not None else hdul[1].header
                    wl_val = int(hdr.get('WAVELNTH', 0))
                    if wl_val in wavelengths:
                        wl = wl_val
            except Exception:
                pass

        if wl is not None and wl in wavelengths:
            wl_file_map[wl] = fpath

    missing = set(wavelengths) - set(wl_file_map.keys())
    if missing:
        raise FileNotFoundError(
            f"Missing FITS files for wavelengths: {sorted(missing)}\n"
            f"Found: {wl_file_map}\n"
            f"Files need wavelength in filename or WAVELNTH header."
        )

    # Load all channels
    headers = []
    first_data, first_hdr = _load_fits_image(wl_file_map[wavelengths[0]])
    ny, nx = first_data.shape
    nwl = len(wavelengths)

    dn_cube = np.zeros((ny, nx, nwl), dtype=np.float64)
    edn_cube = np.zeros((ny, nx, nwl), dtype=np.float64)

    for i, wl in enumerate(wavelengths):
        if i == 0:
            data, hdr = first_data, first_hdr
        else:
            data, hdr = _load_fits_image(wl_file_map[wl])

        if data.shape != (ny, nx):
            raise ValueError(
                f"Shape mismatch: {wl}Å is {data.shape} but {wavelengths[0]}Å is ({ny},{nx})"
            )

        hdr['WAVELNTH'] = wl
        dn_cube[:, :, i] = data
        edn_cube[:, :, i] = _estimate_aia_error(data, hdr)
        headers.append(hdr)

    dn_cube, edn_cube = _clean_data(dn_cube, edn_cube)

    return {
        'dn_cube': dn_cube,
        'edn_cube': edn_cube,
        'wavelengths': wavelengths,
        'headers': headers,
        'format': 'fits',
        'files': wl_file_map,
    }


def _clean_data(dn_cube, edn_cube):
    """Replace NaN with 0, clamp negatives, ensure error floor."""
    nan_count = np.sum(np.isnan(dn_cube))
    neg_count = np.sum(dn_cube < 0)

    if nan_count > 0:
        print(f"[loader] NaN → 0 대체: {nan_count}개 값")
    if neg_count > 0:
        print(f"[loader] 음수 → 0 클램핑: {neg_count}개 값")

    dn_cube = np.nan_to_num(dn_cube, nan=0.0, posinf=0.0, neginf=0.0)
    dn_cube = np.maximum(dn_cube, 0.0)

    edn_cube = np.nan_to_num(edn_cube, nan=1.0, posinf=1.0, neginf=1.0)
    edn_cube = np.maximum(edn_cube, 0.01)

    return dn_cube, edn_cube


def load_response(response_dir, wavelengths=None, logt_range=(5.6, 7.0), nt=42):
    """Load or generate temperature response functions.

    Tries in order:
    1. tresp.npy + tresp_logt.npy in response_dir
    2. Single .npz with 'tresp' and 'tresp_logt' keys
    3. Auto-generate via aiapy (requires network + aiapy installed)

    Parameters
    ----------
    response_dir : str
        Directory to search for response files.
    wavelengths : list of int or None
        Wavelengths. Default: AIA_WAVELENGTHS.
    logt_range : tuple of float
        (min, max) of log10(T) for response. Default (5.6, 7.0).
    nt : int
        Number of temperature bins for interpolation.

    Returns
    -------
    dict with keys:
        'tresp'      : ndarray, shape (nt_resp, nwl) — response functions
        'tresp_logt' : ndarray, shape (nt_resp,) — log10(T) array
        'temps'      : ndarray, shape (nt+1,) — temperature bin edges [K] (for DEMreg)
        'logt'       : ndarray, shape (nt,) — log10(T) bin centers (for SITES)
        'delta_temp' : ndarray, shape (nt,) — bin widths [K] (for SITES)
        'source'     : str — 'file' or 'aiapy'
    """
    if wavelengths is None:
        raise ValueError(
            "wavelengths must be specified explicitly.\n"
            "예: wavelengths=[94,131,171,193,211,335] (AIA)\n"
            "    wavelengths=[94,131,174,193,211,335] (EUI-FSI)\n"
            "사용자에게 기기/파장을 먼저 확인하세요."
        )

    # --- Try loading from files ---
    tresp_path = os.path.join(response_dir, 'tresp.npy')
    logt_path = os.path.join(response_dir, 'tresp_logt.npy')

    if os.path.exists(tresp_path) and os.path.exists(logt_path):
        tresp = np.load(tresp_path).astype(np.float64)
        tresp_logt = np.load(logt_path).astype(np.float64)
        return _build_response_dict(tresp, tresp_logt, logt_range, nt, 'file')

    # Try .npz
    npz_files = glob.glob(os.path.join(response_dir, '*.npz'))
    for npz_path in npz_files:
        data = np.load(npz_path)
        if 'tresp' in data and 'tresp_logt' in data:
            tresp = data['tresp'].astype(np.float64)
            tresp_logt = data['tresp_logt'].astype(np.float64)
            return _build_response_dict(tresp, tresp_logt, logt_range, nt, 'file')

    # Try individual response_94.npy etc.
    resp_map = {}
    for fpath in glob.glob(os.path.join(response_dir, '*.npy')):
        if 'tresp_logt' in os.path.basename(fpath):
            continue
        wl = _extract_wavelength(fpath)
        if wl is not None and wl in wavelengths:
            resp_map[wl] = fpath

    if 'tresp_logt' not in os.path.basename(logt_path) and os.path.exists(logt_path):
        pass  # already tried above

    # If individual response files + logt file
    logt_candidates = glob.glob(os.path.join(response_dir, '*logt*.npy'))
    if len(resp_map) >= len(wavelengths) and logt_candidates:
        tresp_logt = np.load(logt_candidates[0]).astype(np.float64)
        nt_resp = len(tresp_logt)
        nwl = len(wavelengths)
        tresp = np.zeros((nt_resp, nwl), dtype=np.float64)
        for i, wl in enumerate(wavelengths):
            tresp[:, i] = np.load(resp_map[wl]).astype(np.float64)
        return _build_response_dict(tresp, tresp_logt, logt_range, nt, 'file')

    # --- Fallback: bundled response (core/response/) ---
    bundled_dir = os.path.join(os.path.dirname(__file__), 'response')
    instrument = detect_instrument(wavelengths)

    # Pick bundled response based on instrument
    if instrument == 'EUI':
        bundled_npz = os.path.join(bundled_dir, 'eui_response.npz')
        bundled_tresp = os.path.join(bundled_dir, 'tresp_eui.npy')
        label = 'EUI (FSI 174, factor 0.7)'
    else:
        bundled_npz = os.path.join(bundled_dir, 'aia_response.npz')
        bundled_tresp = os.path.join(bundled_dir, 'tresp_aia.npy')
        label = 'AIA'

    bundled_logt = os.path.join(bundled_dir, 'tresp_logt.npy')

    if os.path.exists(bundled_npz):
        data = np.load(bundled_npz)
        tresp = data['tresp'].astype(np.float64)
        tresp_logt = data['tresp_logt'].astype(np.float64)
        print(f"[loader] 번들 {label} 응답 함수 사용: {bundled_npz}")
        print(f"[loader]   shape: ({tresp.shape[0]} temp bins, {tresp.shape[1]} channels)")
        print(f"[loader]   log T: {tresp_logt[0]:.1f}–{tresp_logt[-1]:.1f}")
        return _build_response_dict(tresp, tresp_logt, logt_range, nt, f'bundled_{instrument.lower()}')

    if os.path.exists(bundled_tresp) and os.path.exists(bundled_logt):
        tresp = np.load(bundled_tresp).astype(np.float64)
        tresp_logt = np.load(bundled_logt).astype(np.float64)
        print(f"[loader] 번들 {label} 응답 함수 사용: {bundled_tresp}")
        return _build_response_dict(tresp, tresp_logt, logt_range, nt, f'bundled_{instrument.lower()}')

    raise FileNotFoundError(
        f"No response function files found in {response_dir}\n"
        f"Expected: tresp.npy + tresp_logt.npy, or a .npz with those keys,\n"
        f"or individual response_94.npy files + logt.npy.\n"
        f"Bundled {label} response also not found at {bundled_dir}"
    )


def _build_response_dict(tresp, tresp_logt, logt_range, nt, source):
    """Build response dict with DEMreg temps and SITES logt/delta_temp."""
    # Temperature bin edges for DEMreg
    temps = np.logspace(logt_range[0], logt_range[1], nt + 1)

    # Temperature bin centers and widths for SITES
    logt = np.linspace(logt_range[0], logt_range[1], nt)
    delta_temp = np.gradient(10.0**logt)

    return {
        'tresp': tresp,
        'tresp_logt': tresp_logt,
        'temps': temps,
        'logt': logt,
        'delta_temp': delta_temp,
        'source': source,
    }
