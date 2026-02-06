# Airflow Architecture for Weather Transit Analysis

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     AIRFLOW ORCHESTRATION                        │
│                                                                   │
│  ┌────────────────┐         ┌────────────────┐                  │
│  │   Scheduler    │────────▶│   Web Server   │                  │
│  │  (Background)  │         │   (Port 8080)  │                  │
│  └────────┬───────┘         └────────────────┘                  │
│           │                                                       │
│           │ Triggers Tasks                                       │
│           ▼                                                       │
│  ┌─────────────────────────────────────────────────────┐        │
│  │              LocalExecutor                           │        │
│  │  (Runs tasks in separate processes)                 │        │
│  └─────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Executes
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WEATHER TRANSIT PIPELINE                      │
│                                                                   │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │ Fetch Weather    │         │ Fetch Transit    │             │
│  │ Data (NOAA)      │         │ Data (GTFS)      │             │
│  │                  │         │                  │             │
│  │ • Temperature    │         │ • Routes         │             │
│  │ • Precipitation  │         │ • Schedules      │             │
│  │ • Snowfall       │         │ • Delays         │             │
│  │ • Wind Speed     │         │ • Trips          │             │
│  └────────┬─────────┘         └────────┬─────────┘             │
│           │                            │                         │
│           └──────────┬─────────────────┘                         │
│                      │                                           │
│                      ▼                                           │
│           ┌──────────────────────┐                              │
│           │   Process & Combine  │                              │
│           │                      │                              │
│           │ • Merge datasets     │                              │
│           │ • Clean data         │                              │
│           │ • Calculate metrics  │                              │
│           │ • Add derived fields │                              │
│           └──────────┬───────────┘                              │
│                      │                                           │
│                      ▼                                           │
│           ┌──────────────────────┐                              │
│           │    Run Analysis      │                              │
│           │                      │                              │
│           │ • Statistical tests  │                              │
│           │ • Correlations       │                              │
│           │ • Visualizations     │                              │
│           │ • Generate reports   │                              │
│           └──────────┬───────────┘                              │
└──────────────────────┼──────────────────────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │   PostgreSQL   │
              │   weather_db   │
              │                │
              │ • Raw data     │
              │ • Processed    │
              │ • Results      │
              └────────────────┘
```

## Component Details

### 1. Airflow Core Components

#### Scheduler
- **Purpose**: Monitors DAGs and triggers tasks
- **Frequency**: Continuous background process
- **Responsibilities**:
  - Parse DAG files
  - Schedule task execution
  - Monitor task status
  - Handle retries

#### Web Server
- **Purpose**: User interface for monitoring
- **Access**: http://localhost:8080
- **Features**:
  - DAG visualization
  - Task logs
  - Connection management
  - User authentication

#### LocalExecutor
- **Purpose**: Execute tasks in parallel
- **Method**: Separate Python processes
- **Advantages**:
  - Simple setup
  - Good for single-machine deployments
  - Parallel task execution

#### Metadata Database
- **Type**: PostgreSQL
- **Purpose**: Store Airflow state
- **Contents**:
  - DAG definitions
  - Task instances
  - Execution history
  - Connections
  - Variables

### 2. Pipeline Tasks

#### Task 1: Fetch Weather Data
```python
fetch_weather_data()
├── Input: Date, Cities
├── Source: NOAA API / CSV files
├── Output: Weather metrics
└── Duration: ~30 seconds
```

**Data Collected:**
- Temperature (avg, min, max)
- Precipitation (inches)
- Snowfall (inches)
- Wind speed (mph)
- Weather conditions

#### Task 2: Fetch Transit Data
```python
fetch_transit_data()
├── Input: Date, Cities
├── Source: GTFS feeds
├── Output: Transit metrics
└── Duration: ~45 seconds
```

**Data Collected:**
- Route information
- Scheduled times
- Actual arrival times
- Delay calculations
- Trip counts

#### Task 3: Process & Combine
```python
process_data()
├── Input: Weather + Transit data
├── Processing:
│   ├── Merge on date/city
│   ├── Calculate delays
│   ├── Add weather categories
│   └── Derive season
├── Output: Combined dataset
└── Duration: ~20 seconds
```

**Processing Steps:**
1. Join weather and transit data
2. Calculate average delays per route
3. Categorize weather conditions
4. Add temporal features (season, day of week)
5. Handle missing values
6. Validate data quality

#### Task 4: Run Analysis
```python
run_analysis()
├── Input: Combined dataset
├── Analysis:
│   ├── Correlation analysis
│   ├── Statistical tests
│   ├── Trend analysis
│   └── Visualizations
├── Output: Reports & insights
└── Duration: ~60 seconds
```

**Analysis Performed:**
- Weather impact on delays
- City-specific patterns
- Seasonal trends
- Statistical significance tests
- Predictive insights

### 3. Data Flow

```
External Sources          Airflow Tasks           Storage
─────────────────        ──────────────          ────────

┌──────────┐            ┌──────────┐            ┌──────────┐
│   NOAA   │───────────▶│  Fetch   │───────────▶│  Staging │
│   API    │            │ Weather  │            │  Tables  │
└──────────┘            └──────────┘            └──────────┘
                              │                       │
┌──────────┐            ┌──────────┐                 │
│   GTFS   │───────────▶│  Fetch   │────────────────▶│
│  Feeds   │            │ Transit  │                 │
└──────────┘            └──────────┘                 │
                              │                       │
                              ▼                       ▼
                        ┌──────────┐            ┌──────────┐
                        │ Process  │───────────▶│  Final   │
                        │   Data   │            │  Tables  │
                        └──────────┘            └──────────┘
                              │                       │
                              ▼                       │
                        ┌──────────┐                 │
                        │   Run    │◀────────────────┘
                        │ Analysis │
                        └──────────┘
                              │
                              ▼
                        ┌──────────┐
                        │ Reports  │
                        │ & Logs   │
                        └──────────┘
```

## Execution Flow

### Daily Automated Run

```
06:00 AM UTC
    │
    ▼
┌─────────────────┐
│ Scheduler       │
│ Detects trigger │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Create DAG Run Instance         │
│ Execution Date: 2024-01-15      │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Queue Tasks (Parallel)          │
│ • fetch_weather_data            │
│ • fetch_transit_data            │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Wait for Both Tasks Complete    │
│ ✓ Weather: Success (30s)        │
│ ✓ Transit: Success (45s)        │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Execute process_data            │
│ Status: Running...              │
│ Duration: 20s                   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Execute run_analysis            │
│ Status: Running...              │
│ Duration: 60s                   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ DAG Run Complete                │
│ Total Duration: ~2.5 minutes    │
│ Status: Success ✓               │
└─────────────────────────────────┘
```

### Error Handling Flow

```
Task Execution
    │
    ▼
┌─────────────┐
│   Attempt 1 │
└──────┬──────┘
       │
       ├─ Success ──▶ Continue
       │
       └─ Failure
          │
          ▼
    ┌──────────┐
    │ Wait 5min│
    └────┬─────┘
         │
         ▼
    ┌─────────────┐
    │   Attempt 2 │
    └──────┬──────┘
           │
           ├─ Success ──▶ Continue
           │
           └─ Failure
              │
              ▼
        ┌──────────┐
        │ Wait 5min│
        └────┬─────┘
             │
             ▼
        ┌─────────────┐
        │   Attempt 3 │
        └──────┬──────┘
               │
               ├─ Success ──▶ Continue
               │
               └─ Failure
                  │
                  ▼
            ┌──────────┐
            │   Mark   │
            │  Failed  │
            └──────────┘
```

## Deployment Architecture

### Docker Containers

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Host                           │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  airflow-webserver                             │    │
│  │  Port: 8080                                    │    │
│  │  Image: apache/airflow:2.7.0-python3.9        │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  airflow-scheduler                             │    │
│  │  Image: apache/airflow:2.7.0-python3.9        │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  postgres (Airflow metadata)                   │    │
│  │  Port: 5432 (internal)                         │    │
│  │  Image: postgres:13                            │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Shared Volumes:                                        │
│  • ./dags → /opt/airflow/dags                          │
│  • ./logs → /opt/airflow/logs                          │
│  • ../scripts → /opt/airflow/scripts                   │
│  • ../data → /opt/airflow/data                         │
└─────────────────────────────────────────────────────────┘
         │
         │ Connects to
         ▼
┌─────────────────────────────────────────────────────────┐
│  PostgreSQL (weather_db)                                │
│  Host: host.docker.internal:5432                        │
│  Database: weather_db                                   │
└─────────────────────────────────────────────────────────┘
```

## Monitoring & Observability

### Metrics Tracked

1. **DAG Metrics**
   - Run duration
   - Success rate
   - Failure count
   - Schedule adherence

2. **Task Metrics**
   - Execution time
   - Retry count
   - Queue time
   - Resource usage

3. **Data Metrics**
   - Records processed
   - Data quality checks
   - Missing values
   - Anomalies detected

### Logging Hierarchy

```
logs/
├── scheduler/
│   └── latest/
│       └── scheduler.log
├── dag_id=weather_transit_pipeline/
│   ├── run_id=scheduled__2024-01-15/
│   │   ├── task_id=fetch_weather_data/
│   │   │   └── attempt=1.log
│   │   ├── task_id=fetch_transit_data/
│   │   │   └── attempt=1.log
│   │   ├── task_id=process_data/
│   │   │   └── attempt=1.log
│   │   └── task_id=run_analysis/
│   │       └── attempt=1.log
│   └── run_id=manual__2024-01-15/
│       └── ...
```

## Scalability Considerations

### Current Setup (LocalExecutor)
- **Capacity**: 10-20 parallel tasks
- **Best for**: Single machine, moderate workload
- **Limitations**: CPU/memory of host machine

### Future Scaling Options

1. **CeleryExecutor**
   - Multiple worker machines
   - Distributed task execution
   - Message queue (Redis/RabbitMQ)

2. **KubernetesExecutor**
   - Dynamic pod creation
   - Auto-scaling
   - Resource isolation

3. **Cloud Managed**
   - AWS MWAA (Managed Workflows for Apache Airflow)
   - Google Cloud Composer
   - Azure Data Factory

## Security

### Authentication
- Basic auth enabled
- Username/password required
- Session management

### Connections
- Encrypted storage
- Environment variables
- Secrets backend (optional)

### Network
- Internal Docker network
- Exposed ports: 8080 only
- Database connections secured

## Best Practices Implemented

✅ **Idempotency**: Tasks can be re-run safely  
✅ **Retry Logic**: Automatic failure recovery  
✅ **Logging**: Comprehensive task logs  
✅ **Monitoring**: UI-based observability  
✅ **Modularity**: Separate task functions  
✅ **Documentation**: Inline comments and docs  
✅ **Version Control**: DAGs in Git  
✅ **Testing**: DAG validation before deployment  

## Performance Optimization

### Current Optimizations
- Parallel task execution
- Connection pooling
- Efficient data processing
- Minimal data transfer

### Future Improvements
- Task caching
- Incremental processing
- Data partitioning
- Resource allocation tuning

---

**Last Updated**: 2024
**Airflow Version**: 2.7.0
**Python Version**: 3.9
