# Weather Impact on Indian Public Transportation

Analysis of how weather conditions affect public transportation delays across major Indian cities (Delhi, Mumbai, Bangalore).

## Data Collection

### Weather Data
- **Source**: Visual Crossing Weather API
- **Cities**: Delhi, Mumbai, Bangalore
- **Metrics**: Temperature, precipitation, humidity, wind speed
- **Period**: January 2023 - July 2023

### Transit Data
- **Sources**: 
  - Delhi Metro Open Data Portal
  - Mumbai Local (GTFS feeds)
  - Bangalore BMTC
- **Metrics**: Route delays, trip counts

## Setup Instructions

### 1. Get API Key
Sign up for free API key at: https://www.visualcrossing.com/weather-api

### 2. Collect Weather Data
```bash
# Edit scripts/india_data_collection.py and add your API key
python scripts/india_data_collection.py
```

### 3. Setup Database
```bash
# Run in pgAdmin or psql
psql -U postgres -f config/setup_postgres_india.sql
```

### 4. Load Data
```bash
python scripts/india_load_data.py
```

### 5. Run Analysis
```bash
jupyter notebook indian/weather_analysis_india.ipynb
```

## Key Differences from US Analysis

- **No snowfall**: India doesn't experience snow in major cities
- **Monsoon season**: June-September is critical period
- **Heat waves**: Extreme temperatures (>40°C) are significant
- **Humidity**: High humidity (>85%) impacts transit
- **Rainfall intensity**: Uses IMD classification (Light/Moderate/Heavy/Very Heavy)

## Indian Weather Categories

- **Clear**: Normal conditions
- **Light Rain**: 2-10mm precipitation
- **Rainy**: 10-50mm precipitation  
- **Heavy Rain**: >50mm precipitation
- **Extreme Heat**: Temperature >40°C
- **High Humidity**: Humidity >85%

## Seasons

- **Winter**: December-February
- **Summer**: March-May
- **Monsoon**: June-September
- **Post-Monsoon**: October-November

## Expected Findings

- Monsoon season shows highest delays
- Mumbai most affected by rain (coastal city)
- Delhi affected by extreme heat in summer
- Bangalore relatively stable (moderate climate)
