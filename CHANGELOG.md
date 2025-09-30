# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-XX

### Added
- Initial release of camels-attributes package
- Watershed delineation using NLDI API
- Topographic attributes extraction from USGS 3DEP
- Climate indices calculation from GridMET
- Soil characteristics from gNATSGO and POLARIS
- Vegetation metrics from MODIS and NLCD
- Geological properties from GLiM and GLHYMPS (optional)
- Hydrological signatures from USGS NWIS
- Python API via `CamelsExtractor` class
- Command-line interface via `camels-extract` command
- Support for single and multiple gauge processing
- Comprehensive documentation and examples

### Features
- 70+ catchment attributes following CAMELS methodology
- Graceful handling of missing data with default values
- Customizable date ranges for climate and hydrology data
- CSV and JSON export formats
- Batch processing capability

### Dependencies
- Core: numpy, pandas, geopandas, xarray, rioxarray
- HyRiver ecosystem: pynhd, py3dep, pygridmet, pygeohydro
- Remote sensing: pystac-client, planetary-computer
- Optional: pygeoglim (for geological attributes)

### Known Issues
- Large watersheds may require significant processing time
- Some remote sensing products may timeout for complex watersheds
- pygeoglim must be installed separately if not available on PyPI

## [Unreleased]

### Planned
- Caching mechanism for downloaded geospatial data
- Parallel processing for multiple gauges
- Validation against original CAMELS dataset
- Additional vegetation indices (EVI, SAVI)
- Snow cover attributes from MODIS
- Landform classification attributes
- Support for custom attribute plugins
