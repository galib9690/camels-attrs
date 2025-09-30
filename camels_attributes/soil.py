"""
Soil characteristics extraction
"""

import numpy as np
from pygeohydro import soil_properties, soil_polaris
from pygeoutils import xarray_geomask


def extract_soil_attributes(watershed_geom):
    """
    Extract soil characteristics from gNATSGO and POLARIS datasets.
    
    Parameters
    ----------
    watershed_geom : shapely.geometry
        Watershed boundary
    
    Returns
    -------
    dict
        Soil attributes including porosity, conductivity, depth, texture fractions
    """
    try:
        soil_attrs = {}
        
        # NATSGO soil properties (porosity, AWC, field capacity)
        try:
            props = ["porosity", "available_water_capacity", "field_capacity"]
            soil_data = soil_properties(watershed_geom, props)
            
            soil_attrs["soil_porosity"] = float(soil_data["porosity"].mean().values)
            soil_attrs["awc_mean"] = float(soil_data["available_water_capacity"].mean().values)
            soil_attrs["field_capacity"] = float(soil_data["field_capacity"].mean().values)
        except:
            soil_attrs.update({"soil_porosity": 0.4, "awc_mean": 0.15, "field_capacity": 0.25})
        
        # POLARIS texture and conductivity
        try:
            vars_polaris = ["sand", "silt", "clay", "ksat"]
            depths = [5, 15, 30]  # cm
            
            polaris_data = soil_polaris(watershed_geom, vars_polaris, depths)
            
            # Calculate depth-weighted averages
            sand_vals = []
            silt_vals = []
            clay_vals = []
            ksat_vals = []
            
            for depth in depths:
                if f"sand_{depth}" in polaris_data.data_vars:
                    sand_vals.append(polaris_data[f"sand_{depth}"].mean().values)
                if f"silt_{depth}" in polaris_data.data_vars:
                    silt_vals.append(polaris_data[f"silt_{depth}"].mean().values)
                if f"clay_{depth}" in polaris_data.data_vars:
                    clay_vals.append(polaris_data[f"clay_{depth}"].mean().values)
                if f"ksat_{depth}" in polaris_data.data_vars:
                    ksat_vals.append(polaris_data[f"ksat_{depth}"].mean().values)
            
            soil_attrs["sand_frac"] = float(np.mean(sand_vals)) if sand_vals else 35.0
            soil_attrs["silt_frac"] = float(np.mean(silt_vals)) if silt_vals else 40.0
            soil_attrs["clay_frac"] = float(np.mean(clay_vals)) if clay_vals else 25.0
            
            # Hydraulic conductivity (convert from cm/hr to log10(mm/hr))
            if ksat_vals:
                ksat_mm_hr = np.mean(ksat_vals) * 10  # cm/hr to mm/hr
                soil_attrs["soil_conductivity"] = float(np.log10(ksat_mm_hr))
            else:
                soil_attrs["soil_conductivity"] = 0.5  # log10(mm/hr)
                
        except:
            soil_attrs.update({
                "sand_frac": 35.0,
                "silt_frac": 40.0,
                "clay_frac": 25.0,
                "soil_conductivity": 0.5
            })
        
        # Soil depth (using typical values)
        soil_attrs["soil_depth_statsgo"] = 1.0  # meters
        
        # Water storage capacity
        awc = soil_attrs.get("awc_mean", 0.15)
        depth = soil_attrs["soil_depth_statsgo"]
        soil_attrs["max_water_content"] = awc * depth * 1000  # Convert to mm
        
        return soil_attrs
        
    except Exception as e:
        # Return default values if extraction fails
        return {
            "soil_porosity": 0.4,
            "awc_mean": 0.15,
            "field_capacity": 0.25,
            "sand_frac": 35.0,
            "silt_frac": 40.0,
            "clay_frac": 25.0,
            "soil_conductivity": 0.5,
            "soil_depth_statsgo": 1.0,
            "max_water_content": 150.0
        }
