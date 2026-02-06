# Weather Transit Analysis - Project Flow

## System Architecture Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     DOCKER ENVIRONMENT                          │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Apache Airflow (localhost:8080)              │ │
│  │                                                           │ │
│  │  ┌─────────────────┐      ┌─────────────────┐           │ │
│  │  │   Scheduler     │◄────►│   Webserver     │           │ │
│  │  └────────┬────────┘      └─────────────────┘           │ │
│  │           │                                              │ │
│  │           ▼                                              │ │
│  │  ┌─────────────────────────────────────────┐            │ │
│  │  │         DAG Orchestration               │            │ │
│  │  └─────────────────────────────────────────┘            │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Data Pipeline Flow

### 1. US Cities Pipeline (Every 5 minutes)

```
START
  │
  ├─► Task 1: Fetch Weather Data
  │   ├─ API Call: Visual Crossing Weather API
  │   ├─ Cities: Boston, Chicago, New York
  │   ├─ Data: Temperature, Conditions, Precipitation
  │   └─ Output: weather_data.csv
  │
  ├─► Task 2: Fetch Transit Data
  │   ├─ Generate: Realistic delay patterns
  │   ├─ Cities: Boston, Chicago, New York
  │   ├─ Data: Route, Delay minutes, Timestamp
  │   └─ Output: transit_data.csv
  │
  ├─► Task 3: Process Data
  │   ├─ Merge: Weather + Transit by City & Date
  │   ├─ Clean: Remove nulls, validate data
  │   ├─ Transform: Calculate correlations
  │   └─ Load: PostgreSQL (weather_db)
  │
  └─► Task 4: Run Analysis
      ├─ Query: PostgreSQL database
      ├─ Analyze: Weather impact on delays
      ├─ Calculate: Statistics & correlations
      └─ Output: Logs + Visualizations
```

### 2. Indian Cities Pipeline (Daily at 6:30 AM)

```
START
  │
  ├─► Task 1: Fetch Weather Data
  │   ├─ Real Data: Delhi (365 records from API)
  │   ├─ Synthetic: Mumbai, Bangalore
  │   ├─ Data: Temperature, Humidity, Conditions
  │   └─ Output: indian_weather_data.csv
  │
  ├─► Task 2: Fetch Transit Data
  │   ├─ Generate: 731,929 delay records
  │   ├─ Cities: Delhi, Mumbai, Bangalore
  │   ├─ Data: Route, Delay, Weather correlation
  │   └─ Output: indian_transit_data.csv
  │
  ├─► Task 3: Process & Merge
  │   ├─ Combine: 54,825 final records
  │   ├─ Clean: Data validation
  │   └─ Load: PostgreSQL (indian_weather_db)
  │
  └─► Task 4: Statistical Analysis
      ├─ Calculate: Heavy rain = 123% more delays
      ├─ Generate: Correlation matrices
      └─ Output: Analysis results
```

## Data Flow Diagram

```
┌──────────────────┐
│  Weather API     │
│  (Visual Cross.) │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐      ┌──────────────────┐
│  Weather Data    │      │  Transit Data    │
│  - Temperature   │      │  - Route ID      │
│  - Conditions    │      │  - Delay (min)   │
│  - Precipitation │      │  - Timestamp     │
└────────┬─────────┘      └────────┬─────────┘
         │                         │
         └────────┬────────────────┘
                  ▼
         ┌──────────────────┐
         │  Data Processing │
         │  - Merge         │
         │  - Clean         │
         │  - Transform     │
         └────────┬─────────┘
                  ▼
         ┌──────────────────┐
         │   PostgreSQL     │
         │   Database       │
         │  - weather_db    │
         │  - indian_db     │
         └────────┬─────────┘
                  ▼
         ┌──────────────────┐
         │    Analysis      │
         │  - Statistics    │
         │  - Correlations  │
         │  - Visualizations│
         └────────┬─────────┘
                  ▼
         ┌──────────────────┐
         │     Results      │
         │  - Logs          │
         │  - Charts        │
         │  - Reports       │
         └──────────────────┘
```

## Execution Flow

### Step 1: System Startup
```
User runs: START_AIRFLOW.bat
  ↓
Docker Compose initializes services
  ↓
Airflow webserver starts (localhost:8080)
  ↓
Scheduler begins monitoring DAGs
```

### Step 2: DAG Execution
```
Scheduler triggers DAG (based on schedule)
  ↓
Task 1 executes → Success/Failure
  ↓
Task 2 executes → Success/Failure
  ↓
Task 3 executes → Success/Failure
  ↓
Task 4 executes → Success/Failure
  ↓
DAG completes → Log results
```

### Step 3: Data Storage
```
Raw Data → CSV Files (data/ directory)
  ↓
Processed Data → PostgreSQL Tables
  ↓
Analysis Results → Logs + Visualizations
```

## Technology Stack Flow

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                   │
│  - Airflow Web UI (Monitoring & Control)                │
│  - Jupyter Notebooks (Analysis & Visualization)         │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                   │
│  - Apache Airflow (Workflow Management)                 │
│  - Python DAGs (Task Definition)                        │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    PROCESSING LAYER                     │
│  - Pandas (Data Manipulation)                           │
│  - NumPy (Numerical Computing)                          │
│  - SQLAlchemy (Database ORM)                            │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│                     STORAGE LAYER                       │
│  - PostgreSQL (Structured Data)                         │
│  - CSV Files (Raw Data)                                 │
└─────────────────────────────────────────────────────────┘
```

## Key Metrics Flow

```
INPUT DATA
├─ US Cities: 8,338 records
│  ├─ Weather: 3 cities × 365 days
│  └─ Transit: Multiple routes per day
│
└─ Indian Cities: 54,825 records
   ├─ Weather: 2,193 records (365 real Delhi + synthetic)
   └─ Transit: 731,929 delay records

PROCESSING
├─ Data Cleaning: Remove nulls, validate ranges
├─ Data Merging: Join by city + date
└─ Feature Engineering: Calculate correlations

OUTPUT INSIGHTS
├─ US: Snow → 97% more delays
├─ India: Heavy rain → 123% more delays
└─ Statistical significance: p < 0.05
```

## Error Handling Flow

```
Task Execution
  │
  ├─ Success → Continue to next task
  │
  └─ Failure
      ├─ Log error details
      ├─ Retry (up to 3 times)
      ├─ Send alert (if configured)
      └─ Mark DAG as failed
```

## Monitoring Flow

```
Airflow UI Dashboard
  │
  ├─ DAG Status (Running/Success/Failed)
  ├─ Task Duration (Performance metrics)
  ├─ Logs (Detailed execution info)
  └─ Gantt Chart (Timeline visualization)
```

## Quick Reference

**Start System**: `START_AIRFLOW.bat`  
**Access UI**: http://localhost:8080  
**Credentials**: airflow / airflow  
**Database**: localhost:5432 (postgres/postgres)  
**US Pipeline**: Every 5 minutes  
**Indian Pipeline**: Daily at 6:30 AM  
**Total Records**: 63,163 (8,338 US + 54,825 Indian)
