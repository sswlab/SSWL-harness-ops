"""
DEM SITES — Differential Emission Measure inversion package.

Python translation of the IDL DEM SITES package by Huw Morgan
(Aberystwyth University, 2019).

Implements:
- SITES inversion (Morgan 2019, Sol Phys, 294, 135)
- Grid-SITES efficient multi-pixel inversion (Pickering & Morgan 2019, Sol Phys, 294, 136)

Modules
-------
dem_sites : Core SITES DEM inversion for a single pixel.
dem_gridsites : Grid-SITES wrapper for efficient multi-pixel inversion.
dem_aiainterpolresponse_sites : AIA response function interpolation.
dem_openaiafiles_sites : AIA file reading and noise estimation.
robust_min : Robust minimum/maximum of an array.
"""

from .robust_min import robust_min
from .dem_sites import dem_sites
from .dem_gridsites import dem_gridsites
from .dem_aiainterpolresponse_sites import dem_aiainterpolresponse_sites
from .dem_openaiafiles_sites import dem_openaiafiles_sites

__all__ = [
    'robust_min',
    'dem_sites',
    'dem_gridsites',
    'dem_aiainterpolresponse_sites',
    'dem_openaiafiles_sites',
]
