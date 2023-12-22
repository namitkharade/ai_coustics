from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from crawl import run_crawl
from load import run_load
from classify import run_classify
from sqlite import view_db
import config


default_args = {
    'owner': 'namit',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG('ai_coustics_processing',
          default_args=default_args,
          description='ai-coustics processing with Airflow',
          max_active_runs=1,
          #schedule_interval=timedelta(days=1)
          )

# Function to run Python script
def run_python_script(script_name):
    if script_name=='crawl.py':
        run_crawl()
    elif script_name=='load.py':
        run_load()
    elif script_name=='classify.py':
        run_classify(config.db)
    elif script_name=='sqlite.py':
        view_db()
        # pass

# Define tasks
crawl_task = PythonOperator(
    task_id='crawl_freesound',
    python_callable= lambda: run_python_script('crawl.py'),
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_and_process_audio',
    python_callable=lambda: run_python_script('load.py'),
    dag=dag,
)

classify_task = PythonOperator(
    task_id='classify_audio',
    python_callable=lambda: run_python_script('classify.py'),
    dag=dag,
)

db_task = PythonOperator(
    task_id='view_db_entry',
    python_callable=lambda: run_python_script('sqlite.py'),
    dag=dag,
)

# Define task sequence
crawl_task >> load_task >> classify_task >> db_task