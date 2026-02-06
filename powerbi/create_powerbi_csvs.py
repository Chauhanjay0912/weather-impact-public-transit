"""Generate CSV files for Power BI Dashboard from existing data"""
import pandas as pd
import os
from datetime import datetime

# Create output directory
OUTPUT_DIR = 'powerbi_data'
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("Creating Power BI CSV Files")
print("=" * 60)

# Load existing data files
try:
    # US Data
    us_data = pd.read_csv('data/processed/us_fact_daily_delays.csv')
    us_data['date'] = pd.to_datetime(us_data['date'], format='mixed', dayfirst=True)
    print(f"\n[OK] Loaded US data: {len(us_data)} records")
    
    # Indian Data
    india_data = pd.read_csv('data/processed/fact_daily_delays.csv')
    india_data['date'] = pd.to_datetime(india_data['date'], format='mixed', dayfirst=True)
    print(f"[OK] Loaded Indian data: {len(india_data)} records")
    
except Exception as e:
    print(f"[ERROR] Error loading data: {e}")
    exit(1)

# ============================================
# US DASHBOARD CSVs
# ============================================
print("\n[1/2] Creating US Dashboard CSVs...")

# 1. Overview KPIs
us_kpis = pd.DataFrame([{
    'total_days': us_data['date'].nunique(),
    'total_cities': us_data['city'].nunique(),
    'total_routes': us_data['route_id'].nunique(),
    'total_records': len(us_data),
    'overall_avg_delay': round(us_data['avg_delay_minutes'].mean(), 2),
    'max_delay': round(us_data['avg_delay_minutes'].max(), 2),
    'total_trips_analyzed': us_data['total_trips'].sum()
}])
us_kpis.to_csv(f'{OUTPUT_DIR}/us_overview_kpis.csv', index=False)
print("  [OK] us_overview_kpis.csv")

# 2. Weather Impact
us_weather = us_data.groupby('weather_condition').agg({
    'avg_delay_minutes': ['count', 'mean', 'min', 'max', 'std'],
    'total_trips': 'sum'
}).round(2)
us_weather.columns = ['record_count', 'avg_delay', 'min_delay', 'max_delay', 'std_delay', 'total_trips']
us_weather = us_weather.reset_index().sort_values('avg_delay', ascending=False)
us_weather.to_csv(f'{OUTPUT_DIR}/us_weather_impact.csv', index=False)
print("  [OK] us_weather_impact.csv")

# 3. City Performance
us_cities = us_data.groupby('city').agg({
    'route_id': 'nunique',
    'avg_delay_minutes': ['count', 'mean', 'max'],
    'total_trips': 'sum'
}).round(2)
us_cities.columns = ['routes', 'records', 'avg_delay', 'max_delay', 'total_trips']
us_cities = us_cities.reset_index()

# Add weather-specific delays
for weather in ['Snowy', 'Rainy', 'Clear']:
    weather_delays = us_data[us_data['weather_condition'] == weather].groupby('city')['avg_delay_minutes'].mean()
    us_cities[f'avg_delay_{weather.lower()}'] = us_cities['city'].map(weather_delays).round(2)

us_cities.to_csv(f'{OUTPUT_DIR}/us_city_performance.csv', index=False)
print("  [OK] us_city_performance.csv")

# 4. Time Series Daily
us_daily = us_data.groupby('date').agg({
    'avg_delay_minutes': ['count', 'mean'],
    'avg_temp': 'mean',
    'precipitation': 'mean',
    'snowfall': 'mean',
    'total_trips': 'sum'
}).round(2)
us_daily.columns = ['records', 'avg_delay', 'avg_temp', 'avg_precipitation', 'avg_snowfall', 'total_trips']
us_daily = us_daily.reset_index()
us_daily.to_csv(f'{OUTPUT_DIR}/us_time_series_daily.csv', index=False)
print("  [OK] us_time_series_daily.csv")

# 5. Time Series Monthly
us_data['month'] = us_data['date'].dt.to_period('M').dt.to_timestamp()
us_monthly = us_data.groupby('month').agg({
    'avg_delay_minutes': ['count', 'mean'],
    'avg_temp': 'mean',
    'precipitation': 'sum',
    'snowfall': 'sum',
    'total_trips': 'sum'
}).round(2)
us_monthly.columns = ['records', 'avg_delay', 'avg_temp', 'total_precipitation', 'total_snowfall', 'total_trips']
us_monthly = us_monthly.reset_index()
us_monthly.to_csv(f'{OUTPUT_DIR}/us_time_series_monthly.csv', index=False)
print("  [OK] us_time_series_monthly.csv")

# 6. Route Performance
us_routes = us_data.groupby(['route_id', 'route_name', 'city']).agg({
    'avg_delay_minutes': ['count', 'mean', 'max'],
    'total_trips': 'sum',
    'date': 'nunique'
}).round(2)
us_routes.columns = ['records', 'avg_delay', 'max_delay', 'total_trips', 'days_tracked']
us_routes = us_routes.reset_index().sort_values('avg_delay', ascending=False)
us_routes.to_csv(f'{OUTPUT_DIR}/us_route_performance.csv', index=False)
print("  [OK] us_route_performance.csv")

# 7. Correlation Data
us_corr = us_data[['date', 'city', 'avg_delay_minutes', 'avg_temp', 'precipitation', 
                    'snowfall', 'wind_speed', 'weather_condition', 'season']].copy()
us_corr.to_csv(f'{OUTPUT_DIR}/us_correlation_data.csv', index=False)
print("  [OK] us_correlation_data.csv")

# 8. City-Weather Matrix
us_matrix = us_data.groupby(['city', 'weather_condition']).agg({
    'avg_delay_minutes': ['count', 'mean'],
    'total_trips': 'sum'
}).round(2)
us_matrix.columns = ['occurrences', 'avg_delay', 'total_trips']
us_matrix = us_matrix.reset_index()
us_matrix.to_csv(f'{OUTPUT_DIR}/us_city_weather_matrix.csv', index=False)
print("  [OK] us_city_weather_matrix.csv")

# 9. Seasonal Analysis
us_seasonal = us_data.groupby('season').agg({
    'avg_delay_minutes': ['count', 'mean'],
    'avg_temp': 'mean',
    'precipitation': 'sum',
    'snowfall': 'sum',
    'total_trips': 'sum'
}).round(2)
us_seasonal.columns = ['records', 'avg_delay', 'avg_temp', 'total_precipitation', 'total_snowfall', 'total_trips']
us_seasonal = us_seasonal.reset_index()
season_order = {'Winter': 1, 'Spring': 2, 'Summer': 3, 'Fall': 4}
us_seasonal['order'] = us_seasonal['season'].map(season_order)
us_seasonal = us_seasonal.sort_values('order').drop('order', axis=1)
us_seasonal.to_csv(f'{OUTPUT_DIR}/us_seasonal_analysis.csv', index=False)
print("  [OK] us_seasonal_analysis.csv")

# 10. Top Delays by Weather
us_top = us_data.groupby(['weather_condition', 'route_id', 'route_name', 'city']).agg({
    'avg_delay_minutes': ['mean', 'count']
}).round(2)
us_top.columns = ['avg_delay', 'occurrences']
us_top = us_top.reset_index()
us_top = us_top[us_top['occurrences'] >= 3].sort_values(['weather_condition', 'avg_delay'], ascending=[True, False])
us_top.to_csv(f'{OUTPUT_DIR}/us_top_delays_by_weather.csv', index=False)
print("  [OK] us_top_delays_by_weather.csv")

# ============================================
# INDIAN DASHBOARD CSVs
# ============================================
print("\n[2/2] Creating Indian Dashboard CSVs...")

# 1. Overview KPIs
india_kpis = pd.DataFrame([{
    'total_days': india_data['date'].nunique(),
    'total_cities': india_data['city'].nunique(),
    'total_routes': india_data['route_id'].nunique(),
    'total_records': len(india_data),
    'overall_avg_delay': round(india_data['avg_delay_minutes'].mean(), 2),
    'max_delay': round(india_data['avg_delay_minutes'].max(), 2),
    'total_trips_analyzed': india_data['total_trips'].sum()
}])
india_kpis.to_csv(f'{OUTPUT_DIR}/india_overview_kpis.csv', index=False)
print("  [OK] india_overview_kpis.csv")

# 2. Weather Impact
india_weather = india_data.groupby('weather_condition').agg({
    'avg_delay_minutes': ['count', 'mean', 'min', 'max', 'std'],
    'total_trips': 'sum'
}).round(2)
india_weather.columns = ['record_count', 'avg_delay', 'min_delay', 'max_delay', 'std_delay', 'total_trips']
india_weather = india_weather.reset_index().sort_values('avg_delay', ascending=False)
india_weather.to_csv(f'{OUTPUT_DIR}/india_weather_impact.csv', index=False)
print("  [OK] india_weather_impact.csv")

# 3. City Performance
india_cities = india_data.groupby('city').agg({
    'route_id': 'nunique',
    'avg_delay_minutes': ['count', 'mean', 'max'],
    'total_trips': 'sum'
}).round(2)
india_cities.columns = ['routes', 'records', 'avg_delay', 'max_delay', 'total_trips']
india_cities = india_cities.reset_index()

# Add weather-specific delays
for weather in ['Heavy Rain', 'Rainy', 'Clear']:
    weather_delays = india_data[india_data['weather_condition'] == weather].groupby('city')['avg_delay_minutes'].mean()
    india_cities[f'avg_delay_{weather.lower().replace(" ", "_")}'] = india_cities['city'].map(weather_delays).round(2)

india_cities.to_csv(f'{OUTPUT_DIR}/india_city_performance.csv', index=False)
print("  [OK] india_city_performance.csv")

# 4. Time Series Daily
india_daily = india_data.groupby('date').agg({
    'avg_delay_minutes': ['count', 'mean'],
    'avg_temp': 'mean',
    'humidity': 'mean',
    'total_trips': 'sum'
}).round(2)
india_daily.columns = ['records', 'avg_delay', 'avg_temp', 'avg_humidity', 'total_trips']
india_daily = india_daily.reset_index()
india_daily.to_csv(f'{OUTPUT_DIR}/india_time_series_daily.csv', index=False)
print("  [OK] india_time_series_daily.csv")

# 5. Time Series Monthly
india_data['month'] = india_data['date'].dt.to_period('M').dt.to_timestamp()
india_monthly = india_data.groupby('month').agg({
    'avg_delay_minutes': ['count', 'mean'],
    'avg_temp': 'mean',
    'humidity': 'mean',
    'total_trips': 'sum'
}).round(2)
india_monthly.columns = ['records', 'avg_delay', 'avg_temp', 'avg_humidity', 'total_trips']
india_monthly = india_monthly.reset_index()
india_monthly.to_csv(f'{OUTPUT_DIR}/india_time_series_monthly.csv', index=False)
print("  [OK] india_time_series_monthly.csv")

# 6. Route Performance
india_routes = india_data.groupby(['route_id', 'city']).agg({
    'avg_delay_minutes': ['count', 'mean', 'max'],
    'total_trips': 'sum',
    'date': 'nunique'
}).round(2)
india_routes.columns = ['records', 'avg_delay', 'max_delay', 'total_trips', 'days_tracked']
india_routes = india_routes.reset_index().sort_values('avg_delay', ascending=False)
india_routes.to_csv(f'{OUTPUT_DIR}/india_route_performance.csv', index=False)
print("  [OK] india_route_performance.csv")

# 7. Correlation Data
india_corr = india_data[['date', 'city', 'avg_delay_minutes', 'avg_temp', 
                          'humidity', 'weather_condition']].copy()
india_corr.to_csv(f'{OUTPUT_DIR}/india_correlation_data.csv', index=False)
print("  [OK] india_correlation_data.csv")

# 8. City-Weather Matrix
india_matrix = india_data.groupby(['city', 'weather_condition']).agg({
    'avg_delay_minutes': ['count', 'mean'],
    'total_trips': 'sum'
}).round(2)
india_matrix.columns = ['occurrences', 'avg_delay', 'total_trips']
india_matrix = india_matrix.reset_index()
india_matrix.to_csv(f'{OUTPUT_DIR}/india_city_weather_matrix.csv', index=False)
print("  [OK] india_city_weather_matrix.csv")

# 9. Monsoon Analysis
india_data['monsoon_season'] = india_data['date'].dt.month.apply(
    lambda m: 'Monsoon' if m in [6,7,8,9] else 
              'Winter' if m in [12,1,2] else 
              'Summer' if m in [3,4,5] else 'Post-Monsoon'
)
india_monsoon = india_data.groupby('monsoon_season').agg({
    'avg_delay_minutes': ['count', 'mean'],
    'avg_temp': 'mean',
    'humidity': 'mean',
    'total_trips': 'sum'
}).round(2)
india_monsoon.columns = ['records', 'avg_delay', 'avg_temp', 'avg_humidity', 'total_trips']
india_monsoon = india_monsoon.reset_index()
india_monsoon.columns = ['season', 'records', 'avg_delay', 'avg_temp', 'avg_humidity', 'total_trips']
india_monsoon.to_csv(f'{OUTPUT_DIR}/india_monsoon_analysis.csv', index=False)
print("  [OK] india_monsoon_analysis.csv")

# 10. Top Delays by Weather
india_top = india_data.groupby(['weather_condition', 'route_id', 'city']).agg({
    'avg_delay_minutes': ['mean', 'count']
}).round(2)
india_top.columns = ['avg_delay', 'occurrences']
india_top = india_top.reset_index()
india_top = india_top[india_top['occurrences'] >= 3].sort_values(['weather_condition', 'avg_delay'], ascending=[True, False])
india_top.to_csv(f'{OUTPUT_DIR}/india_top_delays_by_weather.csv', index=False)
print("  [OK] india_top_delays_by_weather.csv")

print("\n" + "=" * 60)
print("[SUCCESS] All CSV files created successfully!")
print(f"Location: {os.path.abspath(OUTPUT_DIR)}")
print("=" * 60)
print(f"\nUS Dashboard: 10 CSV files")
print(f"Indian Dashboard: 10 CSV files")
print(f"\nTotal: 20 CSV files ready for Power BI")
print("\nNext Steps:")
print("1. Open Power BI Desktop")
print("2. Get Data -> Text/CSV")
print("3. Load files from powerbi_data/ folder")
print("4. Follow dashboard_specification.md")
