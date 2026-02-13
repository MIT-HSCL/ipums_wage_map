import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

# Read fixed-width IPUMS data
colspecs = [
    (54, 56),   # STATEFIP
    (56, 61),   # PUMA
    (72, 82),   # PERWT
    (92, 94),   # WKSWORK1
    (94, 96),   # UHRSWORK
    (96, 102),  # INCWAGE
]
names = ['STATEFIP', 'PUMA', 'PERWT', 'WKSWORK1', 'UHRSWORK', 'INCWAGE']

print("Reading IPUMS data...")
df = pd.read_fwf('usa_00002.dat', colspecs=colspecs, names=names, dtype=str)

# Convert to numeric
for col in names:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Filter valid records
df = df[(df['WKSWORK1'] > 0) & (df['UHRSWORK'] > 0) & (df['INCWAGE'] > 0)]

# Calculate hourly wage
df['hourly_wage'] = df['INCWAGE'] / (df['UHRSWORK'] * df['WKSWORK1'])

# Create PUMA identifier (STATEFIP + PUMA)
df['GEOID'] = df['STATEFIP'].astype(int).astype(str).str.zfill(2) + df['PUMA'].astype(int).astype(str).str.zfill(5)

# Calculate weighted mean hourly wage by PUMA
print("Calculating weighted hourly wages by PUMA...")
puma_wages = df.groupby('GEOID').apply(
    lambda x: np.average(x['hourly_wage'], weights=x['PERWT'])
).reset_index(name='avg_hourly_wage')

# Save to CSV
print("Saving results to CSV...")
puma_wages.to_csv('puma_hourly_wages.csv', index=False)
print(f"Saved {len(puma_wages)} PUMA wage calculations to puma_hourly_wages.csv")

# Show summary statistics
print("\nSummary Statistics:")
print(f"Mean hourly wage: ${puma_wages['avg_hourly_wage'].mean():.2f}")
print(f"Median hourly wage: ${puma_wages['avg_hourly_wage'].median():.2f}")
print(f"Min hourly wage: ${puma_wages['avg_hourly_wage'].min():.2f}")
print(f"Max hourly wage: ${puma_wages['avg_hourly_wage'].max():.2f}")

print("\nTop 10 PUMAs by hourly wage:")
print(puma_wages.nlargest(10, 'avg_hourly_wage'))

print("\nBottom 10 PUMAs by hourly wage:")
print(puma_wages.nsmallest(10, 'avg_hourly_wage'))

print("\nTo create the map, you'll need to:")
print("1. Download PUMA shapefiles from: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html")
print("2. Use the puma_hourly_wages.csv file to join with the shapefile")
print("3. Or use online tools like QGIS or ArcGIS to create the map")
