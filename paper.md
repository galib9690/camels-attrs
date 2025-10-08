---
title: 'camels-attrs: Extracting CAMELS-like Catchment Attributes and Hydrometeorological Data for Any USGS Gauge in the USA'
tags:
  - hydrology
  - catchment attributes
  - CAMELS
  - watershed
  - open data
  - reproducible research
authors:
  - name: Mohammad Galib
    orcid: 0000-0002-XXXX-XXXX
    affiliation: 1
  - name: Venkatesh Merwade
    orcid: 0000-0001-XXXX-XXXX
    affiliation: 1
affiliations:
  - name: Lyles School of Civil Engineering, Purdue University, West Lafayette, IN, USA
    index: 1
date: 2025-10-08
bibliography: paper.bib
---

# Summary

`camels-attrs` is an open-source Python package for extracting comprehensive CAMELS-like catchment attributes and hydrometeorological timeseries for any USGS gauge site in the United States. It automates the extraction of topographic, climatic, soil, vegetation, geological, and hydrological characteristics, following the methodology of the CAMELS (Catchment Attributes and Meteorology for Large-sample Studies) dataset. The package enables reproducible, scalable, and publication-quality watershed characterization for hydrological research, model setup, and large-sample studies.

# Statement of Need

Hydrological modeling and research require detailed, standardized catchment attributes and forcing data. The original CAMELS dataset is limited to a fixed set of USGS basins. `camels-attrs` generalizes this approach, allowing researchers to extract the same suite of attributes for any USGS gauge, supporting new research, model transferability, and reproducibility. The package is designed for ease of use, extensibility, and integration with the broader Python geoscience ecosystem.

# Features

- **Automated Watershed Delineation**: Uses USGS NLDI and 3DEP DEM for precise boundary extraction.
- **Topographic Attributes**: Elevation, slope, drainage area, and more.
- **Climate Indices**: Precipitation, temperature, aridity, seasonality from GridMET.
- **Soil Characteristics**: Texture, porosity, conductivity from gNATSGO and POLARIS.
- **Vegetation Metrics**: LAI, NDVI/GVF, land cover from MODIS and NLCD.
- **Geological Properties**: Lithology and permeability from GLiM and GLHYMPS.
- **Hydrological Signatures**: Flow statistics, baseflow index, event characteristics from USGS NWIS.
- **Hydrometeorological Timeseries**: Daily precipitation, temperature, PET, and more.
- **Comprehensive Visualization**: Publication-ready, multi-panel watershed maps.
- **Batch Processing**: Extract attributes for multiple gauges efficiently.
- **Command-line Interface**: For reproducible workflows and automation.

# Implementation

The package is implemented in Python, leveraging the scientific Python stack (numpy, pandas, geopandas, xarray, matplotlib, contextily, cartopy, etc.). It integrates with open data APIs (USGS NLDI, NWIS, GridMET, gNATSGO, POLARIS, GLiM, GLHYMPS) and uses modern geospatial libraries for efficient processing. The codebase is modular, extensible, and fully open source under the MIT license.

# Example

```python
from camels_attrs import CamelsExtractor

extractor = CamelsExtractor('01031500')  # USGS gauge ID
attributes = extractor.extract_all()
extractor.save('attributes.csv')
```

# Acknowledgements

This work was supported by Purdue University and the hydrological research community. We thank the maintainers of the open data sources and the developers of the scientific Python ecosystem.

# References

See `paper.bib` for full references.
