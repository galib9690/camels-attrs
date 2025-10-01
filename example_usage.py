"""
Example usage of the camels-attrs package
"""

from camels_attributes import CamelsExtractor

# Example 1: Extract attributes for a single gauge
print("="*60)
print("Example 1: Single Gauge Extraction")
print("="*60)

gauge_id = "01031500"  # Piscataquis River Near Dover-Foxcroft, Maine
print(f"\nExtracting CAMELS attributes for gauge {gauge_id}...\n")

extractor = CamelsExtractor(gauge_id)
attributes = extractor.extract_all()

print(f"\n{len(attributes)} attributes extracted:")
print("\nSample attributes:")
for key in list(attributes.keys())[:10]:
    print(f"  {key}: {attributes[key]}")

# Save to CSV
extractor.save("example_output.csv")

print("\n" + "="*60)
print("Example 2: Multiple Gauges (see example_multiple.py)")
print("="*60)
print("\nTo extract for multiple gauges, use:")
print("  from camels_attributes import extract_multiple_gauges")
print("  gauges = ['01031500', '02177000', '06803530']")
print("  df = extract_multiple_gauges(gauges)")
print("  df.to_csv('multiple_gauges.csv', index=False)")
