"""
Demo script showing how to use the unified camels_attributes module
with comprehensive visualization capabilities.
"""

from camels_attributes import CamelsExtractor

# Example 1: Simple extraction with comprehensive map
print("=" * 60)
print("DEMO: Comprehensive Watershed Analysis")
print("=" * 60)

gauge_id = "01031500"  # Piscataquis River, Maine

# Create extractor
extractor = CamelsExtractor(gauge_id)

# Extract all attributes
print("\nStep 1: Extracting CAMELS attributes...")
attributes = extractor.extract_all()

# Create comprehensive visualization
print("\nStep 2: Creating comprehensive watershed map...")
fig = extractor.create_comprehensive_map(
    save_path=f'comprehensive_map_{gauge_id}.png',
    show=True
)

print("\n" + "=" * 60)
print("✓ Demo complete!")
print("=" * 60)
print(f"\nGenerated files:")
print(f"  • comprehensive_map_{gauge_id}.png - Multi-panel watershed map")
print(f"\nThe map includes:")
print(f"  • DEM elevation background")
print(f"  • Watershed boundary and stream network")
print(f"  • Gauge location marker")
print(f"  • USA location context")
print(f"  • Comprehensive statistics panel")
print(f"  • Elevation profile")
print(f"  • Land cover pie chart")
print(f"  • Climate water balance")
