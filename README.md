# ai|coustics Data Engineering case study <img align="left" alt="HTML5" width="40px" src="https://github.com/namitkharade/ai_coustics/assets/42877539/81ff161f-c9c0-4879-8557-b39eb8beacce" />

## crawl.py
`crawl.py` is a Python script designed to crawl and download speech data from Freesound. The script's functionality includes:
- Performing a search on Freesound using a query specified in `config.py`.
- Retrieving a specified number of results.
- Downloading each sound result using the `download_sound` function.

## load.py
`load.py` is a Python script for loading audio file information into a database. Its features include:
- Extracting information from each audio file, such as title, file path, and duration, using the `librosa` library.
- Creating a table named `audio_info` in an SQLite database, with fields for ID, title, file path, duration, PESQ score, and quality label.
- Inserting audio file information into the `audio_info` table.
- The script is designed to handle audio files in formats like MP3, WAV, OGG, and FLAC.

## classify.py
`classify.py` is a Python script for classifying speech audio files based on speech quality using the Perceptual Evaluation of Speech Quality (PESQ) metric. Its functionalities include:
- Loading a reference audio file and a degraded (target) audio file using `librosa`.
- Calculating the PESQ score using the `pesq` library, which measures the quality of the target audio compared to the reference.
- Classifying the audio quality based on the PESQ score into categories like "Excellent," "Good," "Fair," or "Poor."
- Connecting to the SQLite database specified in `config.py`.
- Updating the database with PESQ scores and quality classifications.


# Steps to run
### Step 1: Clone Repository
Clone the project repository from the provided GitHub link:
```
git clone https://github.com/namitkharade/ai_coustics.git
```

### Step 2: Initialize Airflow Database
Run the following command to set up the Airflow database:
```
docker compose up airflow-init
```

### Step 3: Build Docker Containers
Build the Docker containers for the application:
```
docker compose up --build
```

### Step 4: Configure Settings
Edit the `config.py` file to set up the necessary configurations. Ensure to include the API key, query terms, desired number of results, and the download folder.

### Step 5: Start Airflow WebUI
The Airflow web user interface (WebUI) will be accessible after running the containers. Open a web browser and go to ```http://localhost:8080``` to access the Airflow WebUI.

### Step 6: Trigger Acoustics Processing DAG
In the Airflow WebUI, locate and trigger the `ai_acoustics_processing` Directed Acyclic Graph (DAG) to initiate the acoustics processing tasks.


## Production Architecture solution:
In a production environment with a focus on scalability, efficiency, and integration with cloud services, using Apache Airflow and Google Cloud Platform can enhance the overall data pipeline.

For the audio files, we can use Google Cloud Storage. It integrates nicely with other GCP services, which is essential for streamlined machine learning workflows. If the metadata is semi-structured and doesn't require complex querying, a NoSQL solution like Google Cloud Firestore or Bigtable can be used. However, if the metadata is highly structured and demands more intricate query capabilities, we can opt for a relational database like BigQuery. GCP also offers various AI and machine learning services, they can directly access data stored in Cloud Storage and metadata in Firestore or BigQuery. 

We can also utilize Airflow to orchestrate the data processing workflows. It is good for automating the pipeline, from managing the extraction of audio, to processing them, and storing the results.
