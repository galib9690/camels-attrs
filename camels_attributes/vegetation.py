"""
Vegetation characteristics extraction
"""

import numpy as np
from pygeohydro import NLCD
from pystac_client import Client
import planetary_computer
import rioxarray


def extract_vegetation_attributes(watershed_geom):
    """
    Extract vegetation characteristics from NLCD and MODIS.
    
    Parameters
    ----------
    watershed_geom : shapely.geometry
        Watershed boundary
    
    Returns
    -------
    dict
        Vegetation attributes including LAI, GVF, land cover fractions
    """
    try:
        veg_attrs = {}
        
        # Microsoft Planetary Computer STAC client
        client = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
        
        # LAI from MODIS (with fallback)
        lai_attrs = extract_modis_lai(client, watershed_geom)
        veg_attrs.update(lai_attrs)
        
        # NDVI/GVF from MODIS (with fallback)
        gvf_attrs = extract_modis_ndvi(client, watershed_geom)
        veg_attrs.update(gvf_attrs)
        
        # Land cover from NLCD
        try:
            nlcd = NLCD()
            lc_data = nlcd.get_map("land_cover", watershed_geom, resolution=30, year=2021)
            
            # Calculate land cover fractions
            unique, counts = np.unique(lc_data.values, return_counts=True)
            total_pixels = np.sum(counts)
            
            # Forest classes: 41, 42, 43
            forest_pixels = np.sum(counts[(unique >= 41) & (unique <= 43)])
            frac_forest = forest_pixels / total_pixels if total_pixels > 0 else 0
            
            # Cropland classes: 81, 82
            crop_pixels = np.sum(counts[(unique >= 81) & (unique <= 82)])
            frac_cropland = crop_pixels / total_pixels if total_pixels > 0 else 0
            
            # Water class: 11
            water_pixels = np.sum(counts[unique == 11])
            water_frac = water_pixels / total_pixels if total_pixels > 0 else 0
            
            # Dominant land cover
            dom_idx = np.argmax(counts)
            dom_code = unique[dom_idx]
            dom_frac = counts[dom_idx] / total_pixels
            
            dom_names = {
                41: "Forest", 42: "Forest", 43: "Forest",
                81: "Cropland", 82: "Cropland",
                71: "Grassland", 52: "Shrubland",
                11: "Water", 90: "Wetland"
            }
            dom_name = dom_names.get(dom_code, f"Class{dom_code}")
            
            veg_attrs.update({
                "frac_forest": float(frac_forest),
                "frac_cropland": float(frac_cropland),
                "water_frac": float(water_frac),
                "dom_land_cover": dom_name,
                "dom_land_cover_frac": float(dom_frac)
            })
            
        except:
            veg_attrs.update({
                "frac_forest": 0.5,
                "frac_cropland": 0.1,
                "water_frac": 0.05,
                "dom_land_cover": "Forest",
                "dom_land_cover_frac": 0.5
            })
        
        # Root depth estimation
        root_depths = estimate_root_depth(veg_attrs.get("dom_land_cover", "Forest"))
        veg_attrs["root_depth_50"] = root_depths[0]
        veg_attrs["root_depth_99"] = root_depths[1]
        
        return veg_attrs
        
    except Exception as e:
        # Return default values
        return {
            "lai_max": 3.0,
            "lai_min": 1.0,
            "lai_diff": 2.0,
            "gvf_max": 0.7,
            "gvf_diff": 0.5,
            "gvf_mean": 0.45,
            "frac_forest": 0.5,
            "frac_cropland": 0.1,
            "water_frac": 0.05,
            "dom_land_cover": "Forest",
            "dom_land_cover_frac": 0.5,
            "root_depth_50": 0.4,
            "root_depth_99": 1.0
        }


def extract_modis_lai(client, watershed_geom):
    """Extract LAI from MODIS with fallback defaults."""
    try:
        search = client.search(
            collections=["modis-15A2H-061"],
            bbox=watershed_geom.bounds,
            datetime="2020-01-01/2020-12-31"
        )
        items = list(search.get_items())
        
        if items:
            item = planetary_computer.sign(items[0])
            lai_asset = item.assets["Lai_500m"]
            lai = rioxarray.open_rasterio(lai_asset.href, masked=True)
            lai_clipped = lai.rio.clip([watershed_geom], crs="EPSG:4326", drop=True, invert=False)
            
            lai_clipped = lai_clipped * 0.1  # Scale factor
            lai_clipped = lai_clipped.where(lai_clipped <= 10)
            
            return {
                "lai_max": float(lai_clipped.max().values),
                "lai_min": float(lai_clipped.min().values),
                "lai_diff": float(lai_clipped.max().values - lai_clipped.min().values)
            }
    except:
        pass
    
    return {"lai_max": 3.0, "lai_min": 1.0, "lai_diff": 2.0}


def extract_modis_ndvi(client, watershed_geom):
    """Extract NDVI/GVF from MODIS with fallback defaults."""
    try:
        search = client.search(
            collections=["modis-13Q1-061"],
            bbox=watershed_geom.bounds,
            datetime="2020-01-01/2020-12-31"
        )
        items = list(search.get_items())
        
        if items:
            item = planetary_computer.sign(items[0])
            ndvi_asset = item.assets["250m_16_days_NDVI"]
            ndvi = rioxarray.open_rasterio(ndvi_asset.href, masked=True)
            ndvi_clipped = ndvi.rio.clip([watershed_geom], crs="EPSG:4326", drop=True, invert=False)
            
            gvf = ndvi_clipped / 10000.0
            gvf = gvf.where((gvf >= -1) & (gvf <= 1))
            
            return {
                "gvf_max": float(gvf.max().values),
                "gvf_diff": float(gvf.max().values - gvf.min().values),
                "gvf_mean": float(gvf.mean().values)
            }
    except:
        pass
    
    return {"gvf_max": 0.7, "gvf_diff": 0.5, "gvf_mean": 0.45}


def estimate_root_depth(land_cover_name):
    """Estimate root depth based on land cover type."""
    root_depth_lookup = {
        "Forest": (0.7, 2.0),
        "Cropland": (0.3, 0.8),
        "Grassland": (0.3, 1.0),
        "Shrubland": (0.4, 1.2),
        "Wetland": (0.2, 0.5),
        "Water": (0.0, 0.0)
    }
    return root_depth_lookup.get(land_cover_name, (0.4, 1.0))
