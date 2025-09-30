"""
Main CAMELS extractor class that orchestrates all attribute extraction
"""

import pandas as pd
from typing import Dict, Optional

from .watershed import delineate_watershed
from .topography import extract_topographic_attributes
from .climate import fetch_climate_data, compute_climate_indices
from .soil import extract_soil_attributes
from .vegetation import extract_vegetation_attributes
from .geology import extract_geological_attributes
from .hydrology import extract_hydrological_signatures


class CamelsExtractor:
    """
    Extract CAMELS-like catchment attributes for any USGS gauge site.
    
    This class provides a simple interface to extract comprehensive catchment
    attributes following the CAMELS methodology.
    
    Parameters
    ----------
    gauge_id : str
        USGS gauge identifier (e.g., '01031500')
    climate_start : str, optional
        Start date for climate data (default: '2000-01-01')
    climate_end : str, optional
        End date for climate data (default: '2020-12-31')
    hydro_start : str, optional
        Start date for streamflow data (default: '2000-01-01')
    hydro_end : str, optional
        End date for streamflow data (default: '2020-12-31')
    
    Examples
    --------
    >>> from camels_attributes import CamelsExtractor
    >>> 
    >>> # Extract attributes for a single gauge
    >>> extractor = CamelsExtractor('01031500')
    >>> attributes = extractor.extract_all()
    >>> 
    >>> # Export to CSV
    >>> df = extractor.to_dataframe()
    >>> df.to_csv('camels_attributes.csv', index=False)
    """
    
    def __init__(
        self,
        gauge_id: str,
        climate_start: str = "2000-01-01",
        climate_end: str = "2020-12-31",
        hydro_start: str = "2000-01-01",
        hydro_end: str = "2020-12-31"
    ):
        self.gauge_id = str(gauge_id)
        self.climate_start = climate_start
        self.climate_end = climate_end
        self.hydro_start = hydro_start
        self.hydro_end = hydro_end
        
        # Initialize storage
        self.watershed_gdf = None
        self.watershed_geom = None
        self.metadata = None
        self.area_km2 = None
        self.attributes = {}
    
    def delineate(self):
        """Delineate watershed boundary."""
        (
            self.watershed_gdf,
            self.watershed_geom,
            self.metadata,
            self.area_km2
        ) = delineate_watershed(self.gauge_id)
        return self.watershed_gdf
    
    def extract_all(self, verbose: bool = True) -> Dict:
        """
        Extract all CAMELS attributes.
        
        Parameters
        ----------
        verbose : bool
            Print progress messages
        
        Returns
        -------
        dict
            Dictionary containing all extracted attributes
        """
        if verbose:
            print(f"Extracting CAMELS attributes for gauge {self.gauge_id}...")
        
        # 1. Watershed delineation
        if verbose:
            print("  [1/7] Delineating watershed...")
        self.delineate()
        
        # 2. Topographic attributes
        if verbose:
            print("  [2/7] Extracting topographic attributes...")
        topo_attrs = extract_topographic_attributes(self.watershed_geom)
        self.attributes.update(topo_attrs)
        
        # 3. Climate indices
        if verbose:
            print("  [3/7] Extracting climate indices...")
        try:
            climate_ds = fetch_climate_data(
                self.watershed_geom, self.climate_start, self.climate_end
            )
            climate_attrs = compute_climate_indices(climate_ds)
            self.attributes.update(climate_attrs)
        except Exception as e:
            if verbose:
                print(f"      Warning: Climate extraction failed - {str(e)}")
        
        # 4. Soil characteristics
        if verbose:
            print("  [4/7] Extracting soil characteristics...")
        try:
            soil_attrs = extract_soil_attributes(self.watershed_geom)
            self.attributes.update(soil_attrs)
        except Exception as e:
            if verbose:
                print(f"      Warning: Soil extraction failed - {str(e)}")
        
        # 5. Vegetation characteristics
        if verbose:
            print("  [5/7] Extracting vegetation characteristics...")
        try:
            veg_attrs = extract_vegetation_attributes(self.watershed_geom)
            self.attributes.update(veg_attrs)
        except Exception as e:
            if verbose:
                print(f"      Warning: Vegetation extraction failed - {str(e)}")
        
        # 6. Geological characteristics
        if verbose:
            print("  [6/7] Extracting geological characteristics...")
        try:
            geol_attrs = extract_geological_attributes(self.watershed_gdf)
            self.attributes.update(geol_attrs)
        except Exception as e:
            if verbose:
                print(f"      Warning: Geology extraction failed - {str(e)}")
        
        # 7. Hydrological signatures
        if verbose:
            print("  [7/7] Computing hydrological signatures...")
        try:
            hydro_attrs = extract_hydrological_signatures(
                self.gauge_id,
                self.watershed_geom,
                self.hydro_start,
                self.hydro_end,
                self.area_km2
            )
            self.attributes.update(hydro_attrs)
        except Exception as e:
            if verbose:
                print(f"      Warning: Hydrology extraction failed - {str(e)}")
        
        # Add metadata
        if self.metadata:
            self.attributes.update({
                "gauge_id": self.metadata["gauge_id"],
                "gauge_name": self.metadata["gauge_name"],
                "gauge_lat": self.metadata["gauge_lat"],
                "gauge_lon": self.metadata["gauge_lon"],
                "huc_02": self.metadata["huc_02"]
            })
        
        if verbose:
            print(f"✓ Extraction complete! {len(self.attributes)} attributes extracted.")
        
        return self.attributes
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert attributes to pandas DataFrame.
        
        Returns
        -------
        pd.DataFrame
            DataFrame with one row containing all attributes
        """
        if not self.attributes:
            raise ValueError("No attributes extracted. Call extract_all() first.")
        
        return pd.DataFrame([self.attributes])
    
    def to_dict(self) -> Dict:
        """
        Get attributes as dictionary.
        
        Returns
        -------
        dict
            Dictionary of all attributes
        """
        return self.attributes.copy()
    
    def save(self, filepath: str, format: str = "csv"):
        """
        Save attributes to file.
        
        Parameters
        ----------
        filepath : str
            Output file path
        format : str
            Output format ('csv' or 'json')
        """
        df = self.to_dataframe()
        
        if format.lower() == "csv":
            df.to_csv(filepath, index=False)
        elif format.lower() == "json":
            df.to_json(filepath, orient="records", indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        print(f"✓ Attributes saved to {filepath}")


def extract_multiple_gauges(gauge_ids: list, **kwargs) -> pd.DataFrame:
    """
    Extract attributes for multiple gauges.
    
    Parameters
    ----------
    gauge_ids : list
        List of USGS gauge identifiers
    **kwargs
        Additional arguments passed to CamelsExtractor
    
    Returns
    -------
    pd.DataFrame
        Combined dataframe with attributes for all gauges
    """
    results = []
    
    for i, gauge_id in enumerate(gauge_ids, 1):
        print(f"\n[{i}/{len(gauge_ids)}] Processing gauge {gauge_id}...")
        try:
            extractor = CamelsExtractor(gauge_id, **kwargs)
            attributes = extractor.extract_all(verbose=False)
            results.append(attributes)
            print(f"  ✓ Success ({len(attributes)} attributes)")
        except Exception as e:
            print(f"  ✗ Failed: {str(e)}")
    
    if results:
        return pd.DataFrame(results)
    else:
        raise Exception("No gauges were successfully processed")
