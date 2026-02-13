# IPUMS USA Hourly Wage Mapping Project

## Summary

This project processes IPUMS USA 2024 ACS microdata and creates a choropleth map of average hourly wages by PUMA (Public Use Microdata Area).

**Hourly Wage Formula**: INCWAGE / (UHRSWORK × WKSWORK1)

## Files

- **create_wage_map.py** - Main script that processes IPUMS data and generates the map
- **puma_hourly_wages.csv** - Calculated average hourly wages for 2,462 PUMAs
- **usa_00002.cbk** - IPUMS codebook describing the data structure
- **usa_hourly_wage_map.svg** - Generated map (not in repo due to size)

## Requirements

- Python 3.x
- pandas
- geopandas
- matplotlib

Install dependencies:
```bash
pip install pandas geopandas matplotlib
```

## Data Requirements

1. **IPUMS USA data extract** (usa_00002.dat) with variables:
   - STATEFIP, PUMA, PERWT, WKSWORK1, UHRSWORK, INCWAGE

2. **PUMA shapefile** (ipums_puma_2020/):
   - Download from IPUMS NHGIS: https://www.nhgis.org/
   - Or Census TIGER/Line: https://www.census.gov/geographies/mapping-files.html

## Usage

```bash
python create_wage_map.py <path_to_puma_shapefile.shp>
```

Example:
```bash
python create_wage_map.py ./ipums_puma_2020/ipums_puma_2020.shp
```

## Results

- **Mean hourly wage**: $40.39
- **Median hourly wage**: $34.51
- **Range**: $18.20 - $3,405.04
- **PUMAs mapped**: 2,462

## Notes

- Uses person weights (PERWT) for proper aggregation
- Extreme values capped at 95th percentile for visualization
- Continental US only (excludes Alaska, Hawaii, Puerto Rico)
- Some extreme values may indicate small sample sizes in certain PUMAs
