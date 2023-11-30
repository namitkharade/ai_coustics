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
2. Run `crawl.py` to initiate the crawling process: `python crawl.py`
3. Run `load.py` to load audio file information into the database: `python load.py`
4. Run `classify.py` to classify speech audio files based on quality: `python classify.py`
