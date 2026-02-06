"""
Export data from PostgreSQL to CSV/Excel for Power BI
Use this as backup if direct PostgreSQL connection fails
"""
import pandas as pd
from sqlalchemy import create_engine
import os

# Database connection
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'weather_db'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

# Create output directory
OUTPUT_DIR = 'powerbi_exports'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Connection string
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

print("=" * 60)
print("Power BI Data Export Utility")
print("=" * 60)

# US Dashboard Views
us_views = [
    'vw_us_overview_kpis',
    'vw_us_weather_impact',
    'vw_us_city_performance',
    'vw_us_time_series_daily',
    'vw_us_time_series_monthly',
    'vw_us_route_performance',
    'vw_us_correlation_data',
    'vw_us_city_weather_matrix',
    'vw_us_seasonal_analysis',
    'vw_us_top_delays_by_weather'
]

# Indian Dashboard Views
india_views = [
    'vw_india_overview_kpis',
    'vw_india_weather_impact',
    'vw_india_city_performance',
    'vw_india_time_series_daily',
    'vw_india_time_series_monthly',
    'vw_india_route_performance',
    'vw_india_correlation_data',
    'vw_india_city_weather_matrix',
    'vw_india_monsoon_analysis',
    'vw_india_top_delays_by_weather'
]

def export_view(view_name, format='csv'):
    """Export a view to CSV or Excel"""
    try:
        df = pd.read_sql(f"SELECT * FROM {view_name}", engine)
        
        if format == 'csv':
            filepath = os.path.join(OUTPUT_DIR, f"{view_name}.csv")
            df.to_csv(filepath, index=False)
        elif format == 'excel':
            filepath = os.path.join(OUTPUT_DIR, f"{view_name}.xlsx")
            df.to_excel(filepath, index=False, engine='openpyxl')
        
        print(f"✓ Exported {view_name}: {len(df)} rows → {filepath}")
        return True
    except Exception as e:
        print(f"✗ Failed to export {view_name}: {e}")
        return False

# Export US views
print("\n[1/2] Exporting US Dashboard Views...")
for view in us_views:
    export_view(view, format='csv')

# Export Indian views
print("\n[2/2] Exporting Indian Dashboard Views...")
for view in india_views:
    export_view(view, format='csv')

# Create combined Excel files
print("\n[3/3] Creating combined Excel workbooks...")

try:
    # US Dashboard Excel
    with pd.ExcelWriter(os.path.join(OUTPUT_DIR, 'US_Dashboard_Data.xlsx'), engine='openpyxl') as writer:
        for view in us_views:
            df = pd.read_sql(f"SELECT * FROM {view}", engine)
            sheet_name = view.replace('vw_us_', '')[:31]  # Excel sheet name limit
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print("✓ Created US_Dashboard_Data.xlsx")
    
    # Indian Dashboard Excel
    with pd.ExcelWriter(os.path.join(OUTPUT_DIR, 'Indian_Dashboard_Data.xlsx'), engine='openpyxl') as writer:
        for view in india_views:
            df = pd.read_sql(f"SELECT * FROM {view}", engine)
            sheet_name = view.replace('vw_india_', '')[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print("✓ Created Indian_Dashboard_Data.xlsx")
    
except Exception as e:
    print(f"✗ Failed to create Excel workbooks: {e}")

print("\n" + "=" * 60)
print("Export Complete!")
print(f"Files saved to: {os.path.abspath(OUTPUT_DIR)}")
print("=" * 60)
print("\nTo use in Power BI:")
print("1. Open Power BI Desktop")
print("2. Get Data → Text/CSV or Excel")
print("3. Navigate to powerbi_exports folder")
print("4. Load the CSV files or Excel workbooks")
print("5. Follow dashboard_specification.md for visualizations")
