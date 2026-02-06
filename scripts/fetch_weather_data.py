"""Fetch weather data from NOAA API"""
import pandas as pd
import requests
from datetime import datetime

def fetch_noaa_weather(cities, date):
    """Fetch weather data for specified cities and date"""
    print(f"Fetching weather data for {cities} on {date}")
    # Placeholder - integrate with actual NOAA API
    # For now, read from existing data
    df = pd.read_csv('/opt/airflow/data/raw/us_weather_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    df_filtered = df[df['date'] == date]
    return df_filtered
