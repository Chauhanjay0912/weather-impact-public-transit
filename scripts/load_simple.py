import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv('data/processed/us_fact_daily_delays.csv')
print(f"Loaded {len(df)} rows from CSV")

# Connect to PostgreSQL
engine = create_engine('postgresql://postgres:postgres@localhost:5432/weather_db')

# Load to database
df.to_sql('transport_delays', engine, if_exists='replace', index=False)
print("Data loaded to PostgreSQL successfully!")
