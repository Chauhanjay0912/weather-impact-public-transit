# Power BI Dashboard - CSV Files

## Quick Start

### Step 1: Load CSV Files in Power BI

1. **Open Power BI Desktop**
2. **File** → **Options** → **Data Load**
3. **Uncheck**: "Autodetect new relationships"
4. **OK**

### Step 2: Import Data

1. **Home** → **Get Data** → **Text/CSV**
2. Navigate to: `powerbi_data` folder
3. **Load each file**:
   - us_overview_kpis.csv
   - us_weather_impact.csv
   - us_city_performance.csv
   - us_time_series_daily.csv
   - us_time_series_monthly.csv
   - us_route_performance.csv
   - us_correlation_data.csv
   - us_city_weather_matrix.csv
   - us_seasonal_analysis.csv
   - us_top_delays_by_weather.csv

### Step 3: Build Dashboard

Follow: `US_Dashboard_Quick_Guide.md`

---

## Dataset Info

**US Data**: 364,038 records (2 years)
- Cities: Boston, Chicago, New York
- Routes: 429
- Days: 731 (Jan 2023 - Dec 2024)

**Indian Data**: 9,125 records
- Cities: Delhi, Mumbai, Bangalore
- Routes: 25

---

## Files

- `powerbi_data/` - CSV files for Power BI
- `US_Dashboard_Quick_Guide.md` - Dashboard build guide
- `dashboard_specification.md` - Detailed design specs
- `dax_measures.txt` - DAX formulas
- `create_powerbi_csvs.py` - Regenerate CSVs

---

## Regenerate Data

```bash
python powerbi/create_powerbi_csvs.py
```

---

## Dashboard Pages

1. **Overview** - KPIs, weather impact, trends
2. **Weather Analysis** - Detailed weather patterns
3. **City Comparison** - City performance metrics
4. **Time Series** - Daily/monthly trends
5. **Route Performance** - Route-level analysis
