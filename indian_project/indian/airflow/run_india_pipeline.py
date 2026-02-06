"""Indian Weather Transit Pipeline"""
import os
import sys
import pandas as pd
from sqlalchemy import create_engine

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

print("=" * 60)
print("Indian Weather Transit Pipeline")
print("=" * 60)

def run_pipeline():
    print("\n[1/4] Loading weather data...")
    weather_df = pd.read_csv('../india_weather_data.csv')
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    print(f"[OK] Loaded {len(weather_df)} weather records")
    
    print("\n[2/4] Loading transit delay data...")
    delays_df = pd.read_csv('../india_delays_performance.csv')
    delays_df['timestamp'] = pd.to_datetime(delays_df['timestamp'])
    delays_df['delay_minutes'] = delays_df['delay_seconds'] / 60
    print(f"[OK] Loaded {len(delays_df)} delay records")
    
    print("\n[3/4] Processing and combining data...")
    daily_delays = delays_df.groupby(['timestamp', 'route_id']).agg({
        'delay_minutes': 'mean',
        'delay_seconds': 'count'
    }).reset_index()
    daily_delays.columns = ['date', 'route_id', 'avg_delay_minutes', 'total_trips']
    
    combined = daily_delays.merge(weather_df, on='date', how='left')
    print(f"[OK] Combined {len(combined)} records")
    
    print("\n[4/4] Loading to PostgreSQL...")
    try:
        engine = create_engine('postgresql://postgres:postgres@localhost:5432/weather_db')
        combined.to_sql('india_transport_delays', engine, if_exists='replace', index=False)
        
        stats = pd.read_sql("""
            SELECT 
                weather_condition,
                COUNT(*) as records,
                ROUND(AVG(avg_delay_minutes)::numeric, 2) as avg_delay
            FROM india_transport_delays
            GROUP BY weather_condition
            ORDER BY avg_delay DESC
        """, engine)
        
        print(f"[OK] Loaded to database")
        print("\nWeather Impact Summary (India):")
        print(stats.to_string(index=False))
        
    except Exception as e:
        print(f"Note: {e}")
    
    print("\n" + "=" * 60)
    print("Pipeline Complete!")
    print("=" * 60)

if __name__ == '__main__':
    run_pipeline()
