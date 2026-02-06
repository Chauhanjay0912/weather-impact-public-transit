import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from scipy import stats

def run_comprehensive_analysis():
    """Run complete analysis on US weather-transit data"""
    
    # Load data
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/weather_db')
    df = pd.read_sql('SELECT * FROM transport_delays', engine)
    df['date'] = pd.to_datetime(df['date'])
    
    print("="*80)
    print("WEATHER IMPACT ON US PUBLIC TRANSPORTATION - ANALYSIS REPORT")
    print("="*80)
    
    # 1. Dataset Overview
    print("\n1. DATASET OVERVIEW")
    print("-" * 80)
    print(f"Total Records: {len(df):,}")
    print(f"Cities: {', '.join(df['city'].unique())}")
    print(f"Date Range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Total Routes: {df['route_id'].nunique()}")
    print(f"Routes by City:")
    for city in df['city'].unique():
        print(f"  - {city}: {df[df['city']==city]['route_id'].nunique()} routes")
    
    # 2. Weather Impact Analysis
    print("\n2. WEATHER IMPACT ANALYSIS")
    print("-" * 80)
    weather_stats = df.groupby('weather_condition')['avg_delay_minutes'].agg(['mean', 'median', 'std', 'count']).sort_values('mean', ascending=False)
    print(weather_stats)
    
    worst_weather = weather_stats.index[0]
    best_weather = weather_stats.index[-1]
    impact_pct = ((weather_stats.loc[worst_weather, 'mean'] - weather_stats.loc[best_weather, 'mean']) / weather_stats.loc[best_weather, 'mean'] * 100)
    print(f"\nKey Finding: {worst_weather} weather causes {impact_pct:.1f}% more delays than {best_weather} weather")
    
    # 3. City Comparison
    print("\n3. CITY PERFORMANCE COMPARISON")
    print("-" * 80)
    city_stats = df.groupby('city')['avg_delay_minutes'].agg(['mean', 'median', 'std', 'count']).sort_values('mean', ascending=False)
    print(city_stats)
    print(f"\nMost Affected City: {city_stats.index[0]} ({city_stats['mean'].iloc[0]:.2f} min avg delay)")
    print(f"Best Performing City: {city_stats.index[-1]} ({city_stats['mean'].iloc[-1]:.2f} min avg delay)")
    
    # 4. Seasonal Analysis
    print("\n4. SEASONAL PATTERNS")
    print("-" * 80)
    seasonal = df.groupby('season')['avg_delay_minutes'].agg(['mean', 'count'])
    seasonal = seasonal.reindex(['Winter', 'Spring', 'Summer', 'Fall'])
    print(seasonal)
    print(f"\nWorst Season: {seasonal['mean'].idxmax()} ({seasonal['mean'].max():.2f} min)")
    print(f"Best Season: {seasonal['mean'].idxmin()} ({seasonal['mean'].min():.2f} min)")
    
    # 5. Precipitation Impact
    print("\n5. PRECIPITATION IMPACT")
    print("-" * 80)
    df['precip_category'] = pd.cut(df['precipitation'], 
                                    bins=[-0.1, 0, 0.1, 0.5, 10], 
                                    labels=['None', 'Light', 'Moderate', 'Heavy'])
    precip_stats = df.groupby('precip_category', observed=True)['avg_delay_minutes'].agg(['mean', 'count'])
    print(precip_stats)
    
    # 6. Temperature Analysis
    print("\n6. TEMPERATURE IMPACT")
    print("-" * 80)
    df['temp_category'] = pd.cut(df['avg_temp'], 
                                  bins=[0, 32, 50, 70, 85, 100], 
                                  labels=['Freezing', 'Cold', 'Mild', 'Warm', 'Hot'])
    temp_stats = df.groupby('temp_category', observed=True)['avg_delay_minutes'].agg(['mean', 'count'])
    print(temp_stats)
    
    # 7. Correlation Analysis
    print("\n7. CORRELATION ANALYSIS")
    print("-" * 80)
    features = ['precipitation', 'snowfall', 'avg_temp', 'wind_speed']
    correlations = {}
    for feature in features:
        corr = df['avg_delay_minutes'].corr(df[feature])
        correlations[feature] = corr
        print(f"{feature:15s}: {corr:+.4f}")
    
    strongest = max(correlations, key=lambda k: abs(correlations[k]))
    print(f"\nStrongest Predictor: {strongest} (r = {correlations[strongest]:.4f})")
    
    # 8. Top Delayed Routes
    print("\n8. TOP 10 MOST DELAYED ROUTES")
    print("-" * 80)
    route_stats = df.groupby(['city', 'route_name'])['avg_delay_minutes'].agg(['mean', 'count'])
    top_routes = route_stats[route_stats['count'] >= 5].sort_values('mean', ascending=False).head(10)
    for idx, (route, row) in enumerate(top_routes.iterrows(), 1):
        print(f"{idx:2d}. {route[0]:10s} - {route[1][:40]:40s} {row['mean']:.2f} min")
    
    # 9. Statistical Significance Testing
    print("\n9. STATISTICAL SIGNIFICANCE TESTS")
    print("-" * 80)
    
    # ANOVA
    groups = [df[df['weather_condition'] == cond]['avg_delay_minutes'] 
              for cond in df['weather_condition'].unique()]
    f_stat, p_value = stats.f_oneway(*groups)
    print(f"ANOVA (Weather Conditions):")
    print(f"  F-statistic: {f_stat:.4f}")
    print(f"  P-value: {p_value:.6f}")
    print(f"  Result: {'SIGNIFICANT' if p_value < 0.05 else 'NOT SIGNIFICANT'} (alpha=0.05)")
    
    # T-test: Snowy vs Clear
    if 'Snowy' in df['weather_condition'].values and 'Clear' in df['weather_condition'].values:
        snowy = df[df['weather_condition'] == 'Snowy']['avg_delay_minutes']
        clear = df[df['weather_condition'] == 'Clear']['avg_delay_minutes']
        t_stat, t_pvalue = stats.ttest_ind(snowy, clear)
        print(f"\nT-Test (Snowy vs Clear):")
        print(f"  T-statistic: {t_stat:.4f}")
        print(f"  P-value: {t_pvalue:.6f}")
        print(f"  Result: {'SIGNIFICANT' if t_pvalue < 0.05 else 'NOT SIGNIFICANT'} (alpha=0.05)")
    
    # 10. Extreme Weather Events
    print("\n10. EXTREME WEATHER EVENTS")
    print("-" * 80)
    extreme = df[(df['precipitation'] > df['precipitation'].quantile(0.95)) | 
                 (df['snowfall'] > 0) | 
                 (df['wind_speed'] > df['wind_speed'].quantile(0.95))]
    normal = df[~df.index.isin(extreme.index)]
    
    print(f"Extreme Weather Days: {len(extreme):,} ({len(extreme)/len(df)*100:.1f}%)")
    print(f"Normal Weather Days: {len(normal):,} ({len(normal)/len(df)*100:.1f}%)")
    print(f"\nAverage Delays:")
    print(f"  Extreme Weather: {extreme['avg_delay_minutes'].mean():.2f} min")
    print(f"  Normal Weather: {normal['avg_delay_minutes'].mean():.2f} min")
    print(f"  Impact: {((extreme['avg_delay_minutes'].mean() - normal['avg_delay_minutes'].mean()) / normal['avg_delay_minutes'].mean() * 100):.1f}% increase")
    
    # 11. Key Performance Indicators
    print("\n11. KEY PERFORMANCE INDICATORS")
    print("-" * 80)
    print(f"Overall Average Delay: {df['avg_delay_minutes'].mean():.2f} minutes")
    print(f"Median Delay: {df['avg_delay_minutes'].median():.2f} minutes")
    print(f"Maximum Delay: {df['avg_delay_minutes'].max():.2f} minutes")
    print(f"Standard Deviation: {df['avg_delay_minutes'].std():.2f} minutes")
    print(f"\nTotal Trips Analyzed: {df['total_trips'].sum():,}")
    print(f"Average Trips per Route per Day: {df['total_trips'].mean():.1f}")
    
    # 12. Summary & Recommendations
    print("\n12. SUMMARY & RECOMMENDATIONS")
    print("-" * 80)
    print("KEY FINDINGS:")
    print(f"1. {worst_weather} weather causes the most delays ({weather_stats.loc[worst_weather, 'mean']:.2f} min avg)")
    print(f"2. {city_stats.index[0]} experiences highest delays ({city_stats['mean'].iloc[0]:.2f} min avg)")
    print(f"3. {strongest.capitalize()} is the strongest weather predictor (r={correlations[strongest]:.3f})")
    print(f"4. {seasonal['mean'].idxmax()} season shows highest delays ({seasonal['mean'].max():.2f} min)")
    print(f"5. Extreme weather increases delays by {((extreme['avg_delay_minutes'].mean() - normal['avg_delay_minutes'].mean()) / normal['avg_delay_minutes'].mean() * 100):.0f}%")
    
    print("\nRECOMMENDATIONS:")
    print("1. Enhance winter operations and snow removal procedures")
    print("2. Implement weather-aware scheduling during forecasted adverse conditions")
    print("3. Focus infrastructure improvements on most-delayed routes")
    print("4. Develop predictive models using snowfall and precipitation data")
    print("5. Increase service frequency during extreme weather events")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    
    # Save summary to file
    with open('../docs/ANALYSIS_SUMMARY.txt', 'w') as f:
        f.write("WEATHER IMPACT ON US PUBLIC TRANSPORTATION - ANALYSIS SUMMARY\n")
        f.write("="*80 + "\n\n")
        f.write(f"Dataset: {len(df):,} records\n")
        f.write(f"Cities: {', '.join(df['city'].unique())}\n")
        f.write(f"Date Range: {df['date'].min().date()} to {df['date'].max().date()}\n\n")
        f.write(f"Worst Weather: {worst_weather} ({weather_stats.loc[worst_weather, 'mean']:.2f} min)\n")
        f.write(f"Most Affected City: {city_stats.index[0]} ({city_stats['mean'].iloc[0]:.2f} min)\n")
        f.write(f"Strongest Predictor: {strongest} (r={correlations[strongest]:.4f})\n")
        f.write(f"Worst Season: {seasonal['mean'].idxmax()} ({seasonal['mean'].max():.2f} min)\n")
    
    print("\nSummary saved to: docs/ANALYSIS_SUMMARY.txt")
    
    return df

if __name__ == "__main__":
    df = run_comprehensive_analysis()
