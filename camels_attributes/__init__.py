"""
CAMELS Attributes Extractor

A Python package for extracting CAMELS-like catchment attributes
for any USGS gauge site in the United States.

Author: Mohammad Galib
Email: mgalib@purdue.edu
"""

__version__ = "0.1.0"
__author__ = "Mohammad Galib"
__email__ = "mgalib@purdue.edu"

from .extractor import CamelsExtractor

__all__ = ["CamelsExtractor"]
