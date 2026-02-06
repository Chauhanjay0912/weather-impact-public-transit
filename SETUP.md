# Complete Setup Guide

## Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Docker Desktop
- Git

## Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/weather-transit-analysis.git
cd weather-transit-analysis
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Setup PostgreSQL

```bash
# Create database
psql -U postgres
CREATE DATABASE weather_db;
\q

# Run schema
psql -U postgres -d weather_db -f config/setup_postgres.sql
```

## Step 4: Configure Environment

Edit `config/.env`:
```
DB_PASSWORD=your_password
```

## Step 5: Load Data

```bash
python scripts/load_simple.py
```

## Step 6: Start Airflow

```bash
cd airflow
docker-compose up -d
```

Access: http://localhost:8080
- Username: `airflow`
- Password: `airflow`

## Step 7: Configure Airflow

1. Admin → Connections → Add
2. Connection Id: `weather_db`
3. Type: `Postgres`
4. Host: `host.docker.internal`
5. Schema: `weather_db`
6. Login: `postgres`
7. Password: `postgres`
8. Port: `5432`

## Step 8: Enable DAGs

Toggle ON:
- `weather_transit_pipeline`
- `weather_analysis_with_notebook`

## Troubleshooting

**Docker not starting:**
- Ensure Docker Desktop is running
- Check port 8080 is free

**Database connection failed:**
- Verify PostgreSQL is running
- Check credentials in config/.env

**DAG not appearing:**
- Wait 1-2 minutes
- Check logs: `docker-compose logs`

## Next Steps

- View analysis: `jupyter notebook notebooks/weather_analysis.ipynb`
- Check results: Query `transport_delays` table
- Monitor pipeline: Airflow UI at localhost:8080
