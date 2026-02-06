"""Weather Analysis Pipeline with Jupyter Notebook"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weather_analysis_with_notebook',
    default_args=default_args,
    description='Run weather analysis including Jupyter notebook',
    schedule_interval='*/2 * * * *',  # Every 2 minutes for demo
    catchup=False,
    tags=['analysis', 'notebook'],
)

# Task 1: Run data pipeline
run_pipeline = PythonOperator(
    task_id='run_data_pipeline',
    python_callable=lambda: print("Data pipeline completed"),
    dag=dag,
)

# Task 2: Run analysis
def run_analysis():
    import pandas as pd
    from sqlalchemy import create_engine
    engine = create_engine('postgresql://postgres:postgres@host.docker.internal:5432/weather_db')
    df = pd.read_sql('SELECT weather_condition, COUNT(*) as records, ROUND(AVG(avg_delay_minutes)::numeric, 2) as avg_delay FROM transport_delays GROUP BY weather_condition ORDER BY avg_delay DESC', engine)
    print("\n=== WEATHER IMPACT ANALYSIS ===")
    print(df.to_string(index=False))
    return df.to_dict()

run_analysis_task = PythonOperator(
    task_id='run_analysis',
    python_callable=run_analysis,
    dag=dag,
)

run_pipeline >> run_analysis_task
