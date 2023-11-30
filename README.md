# Ai_coustics


## crawl.py
`crawl.py` is a Python script designed to crawl and download speech data from the internet, specifically Freesound. The script's functionality includes:

- Performing a search on Freesound using a query specified in `config.py`.
- Retrieving a specified number of results.
- Downloading each sound result using the `download_sound` function.

## load.py
`load.py` is a Python script for loading audio file information into a database. Its features include:

- Extracting information from each audio file, such as title, file path, and duration, using the `librosa` library.
- Creating a table named `audio_info` in an SQLite database, with fields for ID, title, file path, duration, PESQ score, and quality label.
- Inserting audio file information into the `audio_info` table.
- Processing all audio files in a specified directory and inserting their information into the database.
- The script is designed to handle audio files in formats like MP3, WAV, OGG, and FLAC.

## classify.py
`classify.py` is a Python script for classifying speech audio files based on speech quality using the Perceptual Evaluation of Speech Quality (PESQ) metric. Its functionalities include:

- Loading a reference audio file and a degraded (target) audio file using `librosa`.
- Calculating the PESQ score using the `pesq` library, which measures the quality of the target audio compared to the reference.
- Classifying the audio quality based on the PESQ score into categories like "Excellent," "Good," "Fair," or "Poor."
- Connecting to the SQLite database specified in `config.py`.
- Retrieving audio file information.
- Calculating PESQ scores and quality labels for each audio file.
- Updating the database with PESQ scores and quality classifications.


# How to Use
1. Set up the necessary configurations in `config.py` (API key, query terms, desired number of results, download folder).
2. Run `crawl.py` to initiate the crawling process:
   ```
   python crawl.py
   ```
4. Run `load.py` to load audio file information into the database:
   ```
   python load.py
   ```
6. Run `classify.py` to classify speech audio files based on quality:
   ```
   python classify.py
   ```


# Production Architecture:
In a production environment with a focus on scalability, efficiency, and integration with cloud services, incorporating Apache Airflow and Google Cloud Platform (GCP) can enhance the overall data pipeline for crawling, storing, and classifying speech data.

- Use Apache Airflow to schedule and orchestrate the crawling, storing and classifying process. Define an Airflow DAG (Directed Acyclic Graph) that includes tasks for running the `crawl.py`, `load.py` and `classify.py`  script at specified intervals in a given sequence.
- Utilize GCP's Cloud Storage to store the downloaded audio files, leveraging its scalability and durability.
- Integrate with a relational database service, such as PostgreSQL, to store structured metadata.

##Apache Airflow DAG
```
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'namit',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'aicoustics_data_pipeline',
    default_args=default_args,
    description='Speech data pipeline',
    schedule_interval='@daily',
)

crawl_task = PythonOperator(
    task_id='crawl_task',
    python_callable=crawl_function,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_function,
    dag=dag,
)

classify_task = PythonOperator(
    task_id='classify_task',
    python_callable=classify_function,
    dag=dag,
)

# Define task dependencies
crawl_task >> load_task >> classify_task
```


