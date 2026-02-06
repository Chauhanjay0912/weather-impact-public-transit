"""Fetch transit data from GTFS feeds"""
import pandas as pd
from datetime import datetime

def fetch_gtfs_data(cities, date):
    """Fetch GTFS transit data for specified cities and date"""
    print(f"Fetching transit data for {cities} on {date}")
    # Placeholder - integrate with actual GTFS APIs
    # For now, read from existing GTFS data
    all_data = []
    for city in cities:
        city_lower = city.lower().replace(' ', '_')
        try:
            routes = pd.read_csv(f'/opt/airflow/data/raw/gtfs_{city_lower}/routes.txt')
            all_data.append(routes)
        except FileNotFoundError:
            print(f"GTFS data not found for {city}")
    return pd.concat(all_data) if all_data else pd.DataFrame()
