import os
import sqlite3
import librosa
import config

AUDIO_FORMATS = ('.mp3', '.wav', '.ogg', '.flac')
DATABASE_NAME = config.db

#Retrieve audio file information.
def get_audio_info(file_path):
    audio, _ = librosa.load(file_path, sr=None)
    duration = librosa.get_duration(y=audio)
    title = os.path.basename(file_path)
    return title, file_path, duration

#Create the audio_info table in the SQLite database.
def create_audio_info_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            file_path TEXT,
            duration REAL,
            pesq_score REAL,
            quality_label TEXT
        )
    ''')
    conn.commit()

#Insert audio information into the audio_info table.
def insert_audio_info(conn, data):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO audio_info (title, file_path, duration) VALUES (?, ?, ?)', data)
    conn.commit()

#Process audio files in the specified directory and store data in the SQLite table.
def process_audio_files(directory_path):
    print("Processing audio files.........")
    conn = sqlite3.connect(DATABASE_NAME)
    create_audio_info_table(conn)

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(AUDIO_FORMATS):
                file_path = os.path.join(root, file)
                audio_info = get_audio_info(file_path)
                insert_audio_info(conn, audio_info)

    conn.close()

def run_load():
    directory_path = config.folder
    process_audio_files(directory_path)
