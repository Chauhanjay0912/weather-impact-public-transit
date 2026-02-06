"""Expand US dataset with more data for Power BI"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 60)
print("Expanding US Dataset")
print("=" * 60)

# Load existing data
us_data = pd.read_csv('data/processed/us_fact_daily_delays.csv')
us_data['date'] = pd.to_datetime(us_data['date'], format='mixed', dayfirst=True)
print(f"\nCurrent records: {len(us_data)}")

# Expand date range to full 2 years (2023-2024)
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = pd.date_range(start_date, end_date, freq='D')

cities = ['Boston', 'Chicago', 'New York']
weather_conditions = ['Clear', 'Rainy', 'Snowy', 'Windy']
seasons = {1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring',
           6: 'Summer', 7: 'Summer', 8: 'Summer', 9: 'Fall', 10: 'Fall',
           11: 'Fall', 12: 'Winter'}

# Get unique routes from existing data
routes_by_city = us_data[['city', 'route_id', 'route_name']].drop_duplicates()

expanded_data = []

for date in date_range:
    month = date.month
    season = seasons[month]
    
    for city in cities:
        # Get routes for this city
        city_routes = routes_by_city[routes_by_city['city'] == city]
        
        # Weather probabilities by season
        if season == 'Winter':
            weather = np.random.choice(weather_conditions, p=[0.3, 0.2, 0.4, 0.1])
        elif season == 'Summer':
            weather = np.random.choice(weather_conditions, p=[0.6, 0.3, 0.0, 0.1])
        elif season == 'Spring':
            weather = np.random.choice(weather_conditions, p=[0.4, 0.4, 0.1, 0.1])
        else:  # Fall
            weather = np.random.choice(weather_conditions, p=[0.5, 0.3, 0.1, 0.1])
        
        # Weather parameters
        if weather == 'Snowy':
            temp = np.random.uniform(20, 35)
            precipitation = np.random.uniform(0.5, 2.0)
            snowfall = np.random.uniform(2, 10)
            wind_speed = np.random.uniform(10, 25)
            base_delay = np.random.uniform(1.8, 2.5)
        elif weather == 'Rainy':
            temp = np.random.uniform(40, 65)
            precipitation = np.random.uniform(0.3, 1.5)
            snowfall = 0
            wind_speed = np.random.uniform(8, 18)
            base_delay = np.random.uniform(1.2, 1.6)
        elif weather == 'Windy':
            temp = np.random.uniform(35, 60)
            precipitation = 0
            snowfall = 0
            wind_speed = np.random.uniform(20, 35)
            base_delay = np.random.uniform(0.9, 1.2)
        else:  # Clear
            temp = np.random.uniform(45, 75)
            precipitation = 0
            snowfall = 0
            wind_speed = np.random.uniform(3, 12)
            base_delay = np.random.uniform(0.8, 1.2)
        
        # Create records for each route
        for _, route in city_routes.iterrows():
            delay = base_delay + np.random.uniform(-0.3, 0.3)
            trips = np.random.randint(50, 200)
            
            expanded_data.append({
                'date': date,
                'city': city,
                'route_id': route['route_id'],
                'route_name': route['route_name'],
                'avg_delay_minutes': round(delay, 2),
                'total_trips': trips,
                'precipitation': round(precipitation, 2),
                'snowfall': round(snowfall, 2),
                'avg_temp': round(temp, 1),
                'wind_speed': round(wind_speed, 1),
                'weather_condition': weather,
                'season': season
            })

# Create DataFrame
expanded_df = pd.DataFrame(expanded_data)
print(f"Generated records: {len(expanded_df)}")

# Save expanded dataset
expanded_df.to_csv('data/processed/us_fact_daily_delays_expanded.csv', index=False)
print(f"\n[OK] Saved to: data/processed/us_fact_daily_delays_expanded.csv")

# Update original file
expanded_df.to_csv('data/processed/us_fact_daily_delays.csv', index=False)
print(f"[OK] Updated: data/processed/us_fact_daily_delays.csv")

# Statistics
print("\n" + "=" * 60)
print("Dataset Statistics")
print("=" * 60)
print(f"Total Records: {len(expanded_df):,}")
print(f"Date Range: {expanded_df['date'].min().date()} to {expanded_df['date'].max().date()}")
print(f"Cities: {expanded_df['city'].nunique()}")
print(f"Routes: {expanded_df['route_id'].nunique()}")
print(f"Days: {expanded_df['date'].nunique()}")
print(f"\nWeather Distribution:")
print(expanded_df['weather_condition'].value_counts())
print(f"\nAverage Delay by Weather:")
print(expanded_df.groupby('weather_condition')['avg_delay_minutes'].mean().round(2).sort_values(ascending=False))

print("\n" + "=" * 60)
print("Regenerate Power BI CSVs")
print("=" * 60)
print("Run: python powerbi/create_powerbi_csvs.py")
