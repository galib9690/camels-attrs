"""
Demo script showing multi-gauge comparison visualization
Compares attributes across multiple watersheds on US maps
"""

from camels_attrs import create_multi_gauge_comparison

print("=" * 60)
print("DEMO: Multi-Gauge Attribute Comparison")
print("=" * 60)
print()

# Select gauges from different regions
gauge_ids = [
    '01031500',  # Piscataquis River, ME (Northeastern)
    '02177000',  # Edisto River, SC (Southeastern)
    '06803530',  # Salt Creek, NE (Midwestern)
    '08324000',  # Jemez River, NM (Southwestern)
    '11266500',  # Merced River, CA (Western)
]

print(f"Comparing {len(gauge_ids)} watersheds across the USA:")
for gauge_id in gauge_ids:
    print(f"  • {gauge_id}")
print()

# Attributes to compare
attributes_to_plot = ['aridity', 'frac_forest', 'q_mean']

print(f"Creating comparison maps for: {', '.join(attributes_to_plot)}")
print()

# Extract attributes and create comparison map
df, fig = create_multi_gauge_comparison(
    gauge_ids,
    attributes_to_plot=attributes_to_plot,
    n_classes=6,
    colormap='RdYlBu',
    reverse_colormap=True,
    include_histogram=True,
    figure_title='Regional Watershed Characteristics Comparison',
    save_path='multi_gauge_comparison.png'
)

print()
print("=" * 60)
print("✓ Multi-gauge comparison complete!")
print("=" * 60)
print(f"\nGenerated files:")
print(f"  • multi_gauge_comparison.png - Comparison maps")
print()
print("The visualization includes:")
print("  • Side-by-side US maps for each attribute")
print("  • Color-coded catchments by quantile classes")
print("  • Histograms showing distribution")
print("  • Statistical summaries (n, mean, std)")
print()
print("Extracted data available in DataFrame:")
print(df[['gauge_id', 'gauge_name', 'gauge_lat', 'gauge_lon'] + attributes_to_plot].head())
