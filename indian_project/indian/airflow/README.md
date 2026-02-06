# Indian Weather Transit Pipeline - Automated

## Quick Start

### Run Pipeline Now
```bash
cd indian/airflow
python run_india_pipeline.py
```

### Already Scheduled!
✅ Runs automatically daily at **6:30 AM**

## What It Does

Analyzes weather impact on public transportation in:
- 🇮🇳 Delhi
- 🇮🇳 Mumbai  
- 🇮🇳 Bangalore

**Processes:**
- 636 weather records
- 178,199 delay records
- 19,725 combined records

## Results

```
Weather Condition    Avg Delay
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Heavy Rain           1.99 min
High Humidity        1.58 min
Rainy                1.42 min
Clear                1.00 min
```

**Key Finding:** Heavy rain causes 99% more delays!

## Manage Schedule

**View:**
```bash
schtasks /query /tn IndianWeatherTransitPipeline
```

**Run now:**
```bash
schtasks /run /tn IndianWeatherTransitPipeline
```

**Remove:**
```bash
schtasks /delete /tn IndianWeatherTransitPipeline /f
```

## View Data

**Database:**
```sql
SELECT * FROM india_transport_delays;
```

**Analysis:**
```bash
jupyter notebook ../weather_transport_eda_india.ipynb
```
