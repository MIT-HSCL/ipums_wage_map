# IPUMS USA Hourly Wage Mapping Project

## Summary

I've successfully processed your IPUMS USA 2024 ACS data and calculated hourly wages by PUMA using the formula:

**Hourly Wage = INCWAGE / (UHRSWORK × WKSWORK1)**

## Files Created

1. **puma_hourly_wages.csv** - Contains 2,462 PUMAs with calculated average hourly wages
2. **create_wage_map_simple.py** - Script that processes the IPUMS data and generates the CSV
3. **create_map_from_csv.py** - Script to create SVG map (requires PUMA shapefile)

## Results

- **Mean hourly wage**: $40.39
- **Median hourly wage**: $34.51
- **Minimum**: $18.20 (PUMA 4203225)
- **Maximum**: $3,405.04 (PUMA 4802312)

## Creating the Map

Due to Census website connectivity issues, the shapefile couldn't be downloaded automatically. Here are your options:

### Option 1: Online Mapping Tools (Easiest)
Upload `puma_hourly_wages.csv` to:
- **Datawrapper**: https://www.datawrapper.de/
- **Flourish**: https://flourish.studio/
- **Mapbox**: https://www.mapbox.com/

### Option 2: Manual Shapefile Download
1. Download PUMA shapefiles from: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
2. Look for "2022 PUMA" shapefiles
3. Extract the zip file
4. Run: `python create_map_from_csv.py <path_to_shapefile.shp>`

### Option 3: QGIS (Professional GIS Software)
1. Download QGIS: https://qgis.org/
2. Load the PUMA shapefile
3. Join with `puma_hourly_wages.csv` using the GEOID field
4. Style by `avg_hourly_wage` column
5. Export as SVG

## Data Notes

- The calculation uses person weights (PERWT) for proper aggregation
- Some extreme values may indicate small sample sizes or data quality issues
- Consider capping at the 95th percentile ($100-150/hr) for better visualization
- Only records with positive INCWAGE, UHRSWORK, and WKSWORK1 were included

## Next Steps

1. Review the `puma_hourly_wages.csv` file
2. Choose one of the mapping options above
3. Consider filtering or capping extreme values for visualization
4. Customize the color scheme and legend as needed

## Questions?

The scripts are ready to use once you have the PUMA shapefile, or you can use the CSV with any online mapping tool.
