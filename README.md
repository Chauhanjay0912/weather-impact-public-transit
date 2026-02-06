# Weather Impact on Public Transportation

Analysis of how weather conditions affect public transportation delays using real data from US cities.

## 📁 Project Structure

```
├── airflow/           # Apache Airflow orchestration
│   ├── dags/          # Airflow DAG definitions
│   │   └── weather_transit_pipeline.py
│   ├── docker-compose.yml  # Airflow services
│   ├── .env           # Airflow configuration
│   └── README.md      # Airflow setup guide
├── config/            # Configuration files
│   ├── .env           # Environment variables
│   ├── setup_postgres.sql  # Database schema
│   └── postgresql-42.6.0.jar  # JDBC driver
├── data/              # Data files
│   ├── processed/     # Processed datasets
│   └── raw/          # Raw GTFS and weather data
├── docs/             # Documentation
│   ├── QUICKSTART.md  # Quick start guide
│   └── README_SETUP.md  # Detailed setup
├── notebooks/        # Jupyter notebooks
│   └── weather_analysis.ipynb  # Main analysis
├── scripts/          # Python scripts
│   ├── fetch_weather_data.py  # NOAA data fetcher
│   ├── fetch_transit_data.py  # GTFS data fetcher
│   ├── process_data.py        # Data processor
│   ├── run_analysis.py        # Analysis runner
│   └── load_simple.py         # Simple data loader
└── powerbi/          # Power BI integration
```

## 🚀 Quick Start

### Option 1: With Docker Airflow (Automated Pipeline) ⭐ RECOMMENDED

**Prerequisites:** Docker Desktop installed and running

1. **Start Airflow:**
```bash
cd airflow
START_AIRFLOW.bat  # Windows
```

2. **Access Airflow UI** (wait 2-3 minutes):
- URL: http://localhost:8080
- Username: `airflow`
- Password: `airflow`

3. **Configure database connection:**
   - Admin → Connections → Add (+)
   - Connection Id: `weather_db`
   - Type: `Postgres`
   - Host: `host.docker.internal`
   - Schema: `weather_db`
   - Login: `postgres`
   - Password: `postgres`
   - Port: `5432`

4. **Enable DAGs:**
   - Toggle `weather_transit_pipeline` to ON
   - Click ▶ to run immediately
   - Pipelines auto-run every 5 minutes

📚 **Complete guide:** See [DOCKER_AIRFLOW_COMPLETE.md](DOCKER_AIRFLOW_COMPLETE.md)

### Option 2: Manual Analysis

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure database:**
Edit `config/.env` with your PostgreSQL password

3. **Setup PostgreSQL:**
Run SQL from `config/setup_postgres.sql` in pgAdmin

4. **Load data:**
```bash
python scripts/load_simple.py
```

5. **Run analysis:**
```bash
jupyter notebook notebooks/weather_analysis.ipynb
```

## 📊 Key Findings

- **Snowy weather** causes 82% more delays than clear weather
- **Chicago** experiences highest average delays (1.21 min)
- **Snowfall** has strongest correlation (0.34) with delays
- **Winter season** shows 15% increase in delays

## 🛠️ Technologies

- **Python** - Pandas, NumPy, Matplotlib, Seaborn, SciPy
- **PostgreSQL** - Data storage and querying
- **Apache Airflow** - Automated pipeline orchestration
- **Docker** - Containerized Airflow deployment
- **Jupyter** - Interactive analysis and visualization
- **SQLAlchemy** - Database connectivity

## 🔄 Docker Airflow Pipeline

**Automated ETL Pipeline** (runs every 5 minutes):
1. Fetches weather data from CSV files
2. Retrieves transit data from GTFS feeds
3. Processes and combines the datasets
4. Loads data into PostgreSQL
5. Runs comprehensive analysis
6. Shows results in Airflow UI logs

**Features:**
- ✅ Visual pipeline monitoring
- ✅ Real-time task execution
- ✅ Automated scheduling
- ✅ Error handling & retries
- ✅ Web-based logs
- ✅ One-click manual triggers

**Commands:**
```bash
# Start
cd airflow && docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose build && docker-compose up -d
```

See [DOCKER_AIRFLOW_COMPLETE.md](DOCKER_AIRFLOW_COMPLETE.md) for complete guide.

## 📖 Documentation

See `docs/` folder for detailed setup and usage instructions.
