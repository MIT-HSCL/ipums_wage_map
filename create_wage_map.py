import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import sys
import os

# Check if shapefile path is provided
if len(sys.argv) < 2:
    print("Usage: python create_map_from_csv.py <path_to_puma_shapefile>")
    print("\nDownload PUMA shapefiles from:")
    print("https://www2.census.gov/geo/tiger/TIGER2022/PUMA20/")
    print("(Download tl_2022_us_puma20.zip and extract it)")
    sys.exit(1)

shapefile_path = sys.argv[1]

if not os.path.exists(shapefile_path):
    print(f"Error: Shapefile not found at {shapefile_path}")
    sys.exit(1)

# Load wage data
print("Loading wage data...")
puma_wages = pd.read_csv('puma_hourly_wages.csv')

# Load shapefile
print(f"Loading shapefile from {shapefile_path}...")
puma_gdf = gpd.read_file(shapefile_path)

print(f"Shapefile columns: {puma_gdf.columns.tolist()}")

# Find the GEOID column
geoid_col = None
for col in ['GEOID20', 'GEOID10', 'GEOID', 'PUMACE20', 'PUMACE10']:
    if col in puma_gdf.columns:
        geoid_col = col
        break

if geoid_col is None:
    print("Error: Could not find GEOID column in shapefile")
    sys.exit(1)

print(f"Using {geoid_col} for merging")

# Merge - convert to string for compatibility
puma_gdf[geoid_col] = puma_gdf[geoid_col].astype(str)
puma_wages['GEOID'] = puma_wages['GEOID'].astype(str)
puma_gdf = puma_gdf.merge(puma_wages, left_on=geoid_col, right_on='GEOID', how='left')

# Filter to continental US (exclude Alaska, Hawaii, Puerto Rico)
state_col = None
for col in ['STATEFP20', 'STATEFP10', 'STATEFP', 'STATEFIP']:
    if col in puma_gdf.columns:
        state_col = col
        break

if state_col:
    print(f"Filtering using {state_col} column...")
    before = len(puma_gdf)
    puma_gdf = puma_gdf[~puma_gdf[state_col].isin(['02', '15', '72'])]
    print(f"Filtered from {before} to {len(puma_gdf)} PUMAs (removed AK, HI, PR)")
else:
    print("Warning: Could not find state column for filtering")

# Create map
print("Creating map...")
fig, ax = plt.subplots(1, 1, figsize=(20, 12))

# Cap extreme values for better visualization
puma_gdf['wage_capped'] = puma_gdf['avg_hourly_wage'].clip(upper=puma_gdf['avg_hourly_wage'].quantile(0.95))

puma_gdf.plot(
    column='wage_capped',
    ax=ax,
    legend=True,
    cmap='Blues',
    edgecolor='white',
    linewidth=0.1,
    legend_kwds={'label': 'Average Hourly Wage ($)', 'shrink': 0.5}
)

ax.set_title('Average Hourly Wage by PUMA (2024 ACS)', fontsize=16, fontweight='bold')
ax.axis('off')

plt.tight_layout()
plt.savefig('usa_hourly_wage_map.svg', format='svg', dpi=300, bbox_inches='tight')
print("Map saved as usa_hourly_wage_map.svg")
