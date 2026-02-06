"""Process and combine weather and transit data"""
import pandas as pd
from sqlalchemy import create_engine

def process_and_combine_data(date):
    """Combine weather and transit data for specified date"""
    print(f"Processing data for {date}")
    
    # Read processed data
    df = pd.read_csv('/opt/airflow/data/processed/us_fact_daily_delays.csv')
    df['date'] = pd.to_datetime(df['date'])
    df_filtered = df[df['date'] == date]
    
    # Load to staging table
    engine = create_engine('postgresql://postgres:postgres@host.docker.internal:5432/weather_db')
    df_filtered.to_sql('staging_transport_delays', engine, if_exists='replace', index=False)
    
    print(f"Processed {len(df_filtered)} records for {date}")
    return df_filtered
