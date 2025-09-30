# CAMELS Attributes Extractor

## Overview

CAMELS Attributes is a Python package that extracts comprehensive catchment attributes for any USGS gauge site in the United States, following the CAMELS (Catchment Attributes and Meteorology for Large-sample Studies) methodology. The package automates the extraction of 70+ watershed characteristics across multiple domains: topography, climate, soil, vegetation, geology, and hydrology.

**Purpose:** Provide researchers with a reproducible, automated workflow to generate standardized catchment attributes for hydrological modeling and large-sample hydrology studies.

**Author:** Mohammad Galib (mgalib@purdue.edu), Purdue University

**Status:** Production-ready package, complete and ready for PyPI publication

## Recent Changes

**Date:** September 30, 2025

- Created complete package structure for PyPI distribution
- Implemented all 7 core extraction modules (watershed, topography, climate, soil, vegetation, geology, hydrology)
- Fixed critical extractor issues: state management, error tracking, status reporting
- Made pygeoglim an optional dependency with graceful fallbacks
- Added comprehensive documentation (README, INSTALL, HOW_TO_PUBLISH, CHANGELOG)
- Created demo web application to showcase package capabilities
- Package is now ready for `pip install` and distribution

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Design Pattern

The system follows a **modular extraction architecture** where each domain (topography, climate, soil, etc.) is encapsulated in a separate module with standardized interfaces. The `CamelsExtractor` class orchestrates all extractions and handles data aggregation.

**Rationale:** This design allows for independent development and testing of each extraction module, graceful degradation when data sources fail, and easy extension to add new attribute types.

### Data Processing Pipeline

1. **Watershed Delineation** (via NLDI API) → Defines spatial boundary for all subsequent extractions
2. **Parallel Attribute Extraction** → Each domain module fetches and processes data independently
3. **Aggregation & Export** → Results combined into standardized dictionary/DataFrame format

**Key Decision:** Synchronous processing for single gauges with planned async support for batch processing. This simplifies error handling and debugging while maintaining acceptable performance for typical use cases.

### Module Architecture

**Watershed Module (`watershed.py`):**
- Uses NLDI API for automated watershed delineation
- Provides geometry in WGS84 (EPSG:4326) for consistency across APIs
- Calculates watershed area using equal-area projection (EPSG:5070)

**Topography Module (`topography.py`):**
- Fetches DEM from USGS 3DEP via py3dep
- Computes slope using xrspatial
- Handles projection transformations for accurate area calculations

**Climate Module (`climate.py`):**
- Integrates GridMET data for precipitation, temperature, PET
- Computes aridity indices and seasonality metrics
- Supports customizable date ranges (default: 2000-2020)

**Soil Module (`soil.py`):**
- Dual data sources: gNATSGO (porosity, AWC) and POLARIS (texture, conductivity)
- Depth-weighted averaging for subsurface properties
- Fallback to default values on API failures

**Vegetation Module (`vegetation.py`):**
- MODIS data via Microsoft Planetary Computer STAC API for LAI and NDVI
- NLCD for land cover classification
- Timeout handling for large watersheds

**Geology Module (`geology.py`):**
- Optional pygeoglim integration for GLiM and GLHYMPS datasets
- Graceful degradation: returns sensible defaults if package unavailable
- **Design trade-off:** Made optional due to installation complexity vs. value for most users

**Hydrology Module (`hydrology.py`):**
- USGS NWIS for streamflow data
- Baseflow separation and flow signature calculation
- Water balance validation using precipitation data

### Error Handling Strategy

**Approach:** Defensive programming with graceful degradation
- Each module has try-except blocks with fallback values
- Missing optional dependencies (e.g., pygeoglim) return defaults instead of failing
- API timeouts or rate limits trigger retries or default values

**Rationale:** Ensures users get partial results even when some data sources fail, rather than complete failure. Critical for operational workflows.

### CLI and API Design

**Python API:** Object-oriented interface via `CamelsExtractor` class
- Single gauge: `extractor = CamelsExtractor(gauge_id)`
- Batch processing: `extract_multiple_gauges([gauge_ids])`

**CLI:** Command-line tool (`camels-extract`) for non-Python users
- Supports single/multiple gauges
- CSV/JSON output formats
- Date range customization

**Design Decision:** Dual interface allows both programmatic integration and standalone usage, broadening user base.

## External Dependencies

### HyRiver Ecosystem (Core Dependencies)
- **pynhd**: NLDI API client for watershed delineation
- **py3dep**: USGS 3DEP elevation data access
- **pygridmet**: GridMET climate data retrieval
- **pygeohydro**: NWIS streamflow data and soil properties (gNATSGO/POLARIS)
- **pygeoutils**: Geospatial utilities and masking operations

**Rationale:** HyRiver provides unified, well-maintained access to US hydrological datasets with consistent APIs.

### Geospatial Stack
- **geopandas**: Vector data handling and spatial operations
- **xarray/rioxarray**: Raster data processing with CRS-aware operations
- **shapely**: Geometry manipulation
- **rasterio**: Low-level raster I/O

### Remote Sensing
- **pystac-client**: STAC catalog interface for MODIS data
- **planetary-computer**: Microsoft Planetary Computer authentication and access

**Integration Point:** MODIS LAI and NDVI accessed via STAC protocol, allowing for temporal compositing and cloud masking.

### Scientific Computing
- **numpy/pandas**: Numerical operations and data frames
- **scipy**: Statistical functions (curve fitting for climate indices)
- **xrspatial**: Topographic analysis (slope, aspect calculations)

### Hydrological Analysis
- **hydrofunctions**: USGS NWIS data access and streamflow analysis

### Optional Dependencies
- **pygeoglim**: GLiM (lithology) and GLHYMPS (hydrogeological properties)
  - Not on PyPI; requires source installation
  - Package functions without it using default geological values

### External APIs and Data Sources
1. **NLDI API**: Watershed delineation (REST API)
2. **USGS 3DEP**: Elevation data (web service)
3. **GridMET**: Climate reanalysis (OPeNDAP/NetCDF)
4. **USGS NWIS**: Streamflow observations (REST API)
5. **Microsoft Planetary Computer**: MODIS imagery (STAC catalog)
6. **SSURGO/gNATSGO**: Soil databases (web coverage service)
7. **POLARIS**: High-resolution soil properties (cloud-optimized GeoTIFF)

**Dependency Risk Mitigation:** All external data access includes timeout handling and default value fallbacks to prevent cascade failures.

### Build and Distribution
- **setuptools**: Package building (configured via pyproject.toml)
- **build/twine**: PyPI publishing workflow

**Configuration:** Modern pyproject.toml-based setup following PEP 517/518 standards.