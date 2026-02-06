# Weather Transit Pipeline

## Overview
Automated pipeline for analyzing weather impact on public transportation.

## Pipeline Tasks
1. **Fetch Weather Data** - NOAA weather data for Boston, Chicago, New York
2. **Fetch Transit Data** - GTFS transit data from each city
3. **Process Data** - Combines and processes datasets
4. **Run Analysis** - Generates weather impact analysis

## Quick Start

### Run Pipeline Now
```bash
cd airflow
python run_airflow_simple.py
```

### Setup Automated Daily Runs
```bash
cd airflow
setup_schedule.bat
```
Runs daily at 6:00 AM automatically.

## Manage Schedule

**View schedule:**
```bash
schtasks /query /tn WeatherTransitPipeline
```

**Run now:**
```bash
schtasks /run /tn WeatherTransitPipeline
```

**Remove schedule:**
```bash
schtasks /delete /tn WeatherTransitPipeline /f
```

**GUI:**
```bash
taskschd.msc
```

## View Results

**Check logs:**
```bash
type pipeline_log.txt
```

**Query database:**
```bash
psql -h localhost -U postgres -d weather_db
```

**Run analysis:**
```bash
jupyter notebook ../notebooks/weather_analysis.ipynb
```

## File Structure
```
airflow/
├── dags/
│   └── weather_transit_pipeline.py  # Pipeline definition
├── run_airflow_simple.py            # Main runner
├── schedule_pipeline.bat            # Scheduler wrapper
├── setup_schedule.bat               # Setup automation
└── NO_DOCKER_GUIDE.md              # Complete guide
```

## Customization

Edit `dags/weather_transit_pipeline.py` to:
- Change schedule time
- Add more cities
- Modify retry logic
- Add email alerts
