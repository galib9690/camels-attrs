---
title: 'camels-attrs: A Python Package for Extracting CAMELS-like Catchment Attributes and Hydrometeorological Data for Any USGS Gauge in the USA'
tags:
  - Python
  - hydrology
  - catchment attributes
  - CAMELS
  - watershed characterization
  - open data
  - reproducible research
  - hydrological modeling
authors:
  - name: Mohammad Galib
    orcid: 0000-0002-XXXX-XXXX
    equal-contrib: true
    affiliation: 1
  - name: Venkatesh Merwade
    orcid: 0000-0001-XXXX-XXXX
    equal-contrib: false
    affiliation: 1
affiliations:
  - name: Lyles School of Civil Engineering, Purdue University, West Lafayette, IN, USA
    index: 1
date: 8 October 2025
bibliography: paper.bib
---

# Summary

Large-sample hydrology studies and distributed hydrological modeling require comprehensive catchment attributes and hydrometeorological forcing data. The Catchment Attributes and Meteorology for Large-sample Studies (CAMELS) dataset [@addor2017camels; @newman2015development] has become a cornerstone resource, providing standardized attributes for 671 basins across the contiguous United States. However, CAMELS is limited to a pre-selected set of gauges, restricting its applicability to new study sites and emerging research questions.

`camels-attrs` is an open-source Python package that addresses this limitation by enabling the extraction of CAMELS-like attributes for any USGS stream gauge in the United States. The package automates the entire workflow—from watershed delineation to attribute extraction—making it possible to generate standardized catchment characterizations on-demand. This capability is essential for model transferability studies, ungauged basin predictions, and expanding the geographic scope of comparative hydrology research.

# Statement of Need

Hydrological research increasingly relies on large-sample studies to understand catchment behavior across diverse environmental gradients [@gupta2014large]. The original CAMELS dataset revolutionized this field by providing standardized attributes, but its fixed coverage limits: (1) the inclusion of new study sites, (2) temporal updates as data sources improve, (3) customization of attribute extraction methods, and (4) integration with emerging data products.

Existing tools for catchment characterization are typically fragmented across multiple software packages, require manual data collection, or lack standardization. Researchers often spend considerable time assembling attributes from disparate sources, leading to inconsistencies and reduced reproducibility. Several Python packages exist for hydrological data retrieval (e.g., `dataretrieval`, `hydrofunctions`) but none provide comprehensive, CAMELS-consistent attribute extraction.

`camels-attrs` fills this gap by providing:

1. **Automated, reproducible workflows** for extracting 70+ standardized catchment attributes
2. **Integration with authoritative data sources** (USGS, GridMET, gNATSGO, MODIS, NLCD)
3. **Extensibility** for custom attribute definitions and new data sources
4. **Hydrometeorological timeseries extraction** for model forcing
5. **Publication-quality visualization** capabilities
6. **Batch processing** for multiple gauges

The package directly addresses the JOSS scope by solving complex modeling problems in a scientific context, extracting knowledge from large datasets, and enabling new research challenges through standardized, reproducible catchment characterization.

# Related Work and Comparison

Several software packages exist in the hydrological data retrieval space:

- **dataretrieval** [@dataretrieval]: USGS package for retrieving water data, but limited to streamflow observations
- **hydrofunctions** [@hydrofunctions]: Python library for USGS data, focused on timeseries, not catchment attributes  
- **HydroData** suite (`pynhd`, `py3dep`, `pygeohydro`, `pygridmet`) [@hydrodata]: Low-level data access libraries that `camels-attrs` builds upon
- **CAMELS dataset** [@addor2017camels]: Static dataset, not software for on-demand extraction

`camels-attrs` uniquely combines these capabilities into a single, high-level interface specifically designed for CAMELS-consistent attribute extraction, following established methodologies while enabling customization and extension.

# Implementation

## Architecture

The package follows a modular design with specialized modules for each attribute category:

- **watershed.py**: Automated delineation using NLDI and polygon simplification
- **topography.py**: DEM-derived metrics (elevation, slope) using `py3dep`
- **climate.py**: Climate indices from GridMET using `pygridmet`
- **soil.py**: Soil properties from gNATSGO and POLARIS using `pygeohydro`
- **vegetation.py**: Vegetation metrics from MODIS (Planetary Computer) and NLCD
- **geology.py**: Geological attributes from GLiM and GLHYMPS via `pygeoglim`
- **hydrology.py**: Hydrological signatures from USGS NWIS using `hydrofunctions`
- **timeseries.py**: Hydrometeorological forcing data extraction and processing
- **visualization.py**: Multi-panel watershed visualization with DEM, streams, and statistics
- **multi_gauge_viz.py**: Comparative visualization for multiple gauges

## Key Technical Features

1. **Spatial Data Processing**: Leverages `geopandas`, `xarray`, and `rioxarray` for efficient geospatial operations
2. **API Integration**: Connects to multiple authoritative data sources with error handling and retry logic
3. **Computational Efficiency**: Uses spatial masking, chunking, and caching to minimize data transfer
4. **Extensibility**: Modular design allows users to add custom attribute extractors
5. **CLI Integration**: Command-line interface (`camels-extract`) for automated workflows
6. **Visualization**: Publication-ready maps using `matplotlib`, `cartopy`, and `contextily`

## Data Sources

The package integrates the following authoritative data sources:

- **Watershed boundaries**: USGS NLDI (Network-Linked Data Index)
- **Topography**: USGS 3DEP (3D Elevation Program) at 10m resolution
- **Climate**: GridMET (4km daily meteorological data, 1979-present)
- **Soil**: gNATSGO (gridded National Soil Survey Geographic Database) and POLARIS
- **Vegetation**: MODIS (MOD13Q1, MOD15A2H), NLCD (National Land Cover Database)
- **Geology**: GLiM (Global Lithological Map), GLHYMPS (Global Hydrogeology Maps)
- **Streamflow**: USGS NWIS (National Water Information System)

# Example Usage

## Basic Attribute Extraction

```python
from camels_attrs import CamelsExtractor

# Extract attributes for a single gauge
extractor = CamelsExtractor('01031500')
attributes = extractor.extract_all()

# Save to CSV
extractor.save('attributes.csv')

# Or get as DataFrame for analysis
df = extractor.to_dataframe()
print(f"Watershed area: {attributes['area_geospa_fabric']} km²")
print(f"Mean elevation: {attributes['elev_mean']} m")
print(f"Aridity index: {attributes['aridity']}")
```

## Hydrometeorological Timeseries

```python
# Extract daily forcing data
forcing_data = extractor.extract_timeseries('2010-01-01', '2020-12-31')

# Calculate monthly aggregations
from camels_attrs import get_monthly_summary
monthly = get_monthly_summary(forcing_data)

# Calculate water balance
from camels_attrs import calculate_water_balance
water_balance = calculate_water_balance(forcing_data)
```

## Batch Processing

```python
from camels_attrs import extract_multiple_gauges

# Process multiple gauges
gauge_ids = ['01031500', '02177000', '06803530']
df = extract_multiple_gauges(gauge_ids)
df.to_csv('multiple_gauges.csv', index=False)
```

## Visualization

```python
# Create comprehensive watershed map
fig = extractor.create_comprehensive_map(
    save_path='watershed_map.png',
    show=True
)
```

## Command-Line Interface

```bash
# Extract attributes
camels-extract 01031500 -o attributes.csv

# Include timeseries data
camels-extract 01031500 --timeseries --monthly

# Multiple gauges
camels-extract 01031500 02177000 -o combined.csv
```

# Community Guidelines

## Contributing

We welcome contributions from the hydrological community. Please see our GitHub repository for:

- **Issue tracking**: Report bugs or request features
- **Pull requests**: Submit code improvements
- **Documentation**: Help improve tutorials and examples

## Getting Help

- **Documentation**: https://github.com/galib9690/camels-attrs#readme
- **Issues**: https://github.com/galib9690/camels-attrs/issues
- **Examples**: See `example_usage.ipynb` in the repository

## Citation

If you use `camels-attrs` in your research, please cite:

```bibtex
@software{galib2025camelsattrs,
  author = {Galib, Mohammad and Merwade, Venkatesh},
  title = {camels-attrs: CAMELS-like Catchment Attributes Extraction},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/galib9690/camels-attrs}
}
```

# Acknowledgements

This work was supported by the Lyles School of Civil Engineering at Purdue University. We acknowledge the USGS, NOAA, NASA, and other agencies for providing open access to hydrometeorological and geospatial data. We thank the developers and maintainers of the HydroData suite of Python packages (`pynhd`, `py3dep`, `pygeohydro`, `pygridmet`, `pygeoutils`) upon which this package is built. We also thank the broader scientific Python community for developing the foundational libraries (NumPy, pandas, geopandas, xarray, matplotlib) that make this work possible.

# References
