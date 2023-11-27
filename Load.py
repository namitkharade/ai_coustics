import os
from pydub import AudioSegment
import sqlite3

# Function to get audio file information
def get_audio_info(file_path):
    audio = AudioSegment.from_file(file_path)
    title = os.path.basename(file_path)
    duration = len(audio) / 1000  # Convert milliseconds to seconds
    return title, file_path, duration

# Function to create SQLite table
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            file_path TEXT,
            duration REAL
        )
    ''')
    conn.commit()

# Function to insert data into SQLite table
def insert_data(conn, data):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO audio_info (title, file_path, duration) VALUES (?, ?, ?)', data)
    conn.commit()

# Main function to process audio files and store data in SQLite table
def process_audio_files(directory_path):
    conn = sqlite3.connect('audio_info.db')
    create_table(conn)

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                file_path = os.path.join(root, file)
                audio_info = get_audio_info(file_path)
                insert_data(conn, audio_info)

    conn.close()

# Specify the directory path containing audio files
directory_path = r'C:\Users\Namit\Downloads\ai_coustics\files'

# Process audio files and store data in SQLite table
process_audio_files(directory_path)
