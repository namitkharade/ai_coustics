import config
import sqlite3
import librosa
import pesq

REFERENCE_AUDIO_PATH = config.reference_audio
DB_UPDATE_ERROR_MESSAGE = "Error updating database for audio ID {audio_id}: {e}"
PESQ_ERROR_MESSAGE = "Error calculating PESQ score for files {degraded_path}: {e}"

# Function to calculate PESQ score
def calculate_pesq(reference_path, degraded_path):
    try:
        ref_audio, _ = librosa.load(reference_path, sr=None)
        deg_audio, _ = librosa.load(degraded_path, sr=None)

        pesq_score = pesq.pesq(16000, ref_audio, deg_audio, 'wb')
        return pesq_score
    except Exception as e:
        print(PESQ_ERROR_MESSAGE.format(degraded_path=degraded_path, e=e))
        return None

# Function to classify speech quality
def classify_quality(pesq_score):
    if pesq_score is None:
        return "Error"
    elif pesq_score >= 4.5:
        return "Excellent"
    elif pesq_score >= 3.5:
        return "Good"
    elif pesq_score >= 2.5:
        return "Fair"
    else:
        return "Poor"

# Function to update the database
def update_database(database_path):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, file_path FROM audio_info")
        rows = cursor.fetchall()

        for row in rows:
            audio_id, audio_file_path = row

            pesq_score = calculate_pesq(REFERENCE_AUDIO_PATH, audio_file_path)
            quality_label = classify_quality(pesq_score)

            if pesq_score is not None:
                try:
                    cursor.execute("UPDATE audio_info SET pesq_score=?, quality_label=? WHERE id=?", (pesq_score, quality_label, audio_id))
                except Exception as e:
                    print(DB_UPDATE_ERROR_MESSAGE.format(audio_id=audio_id, e=e))

        conn.commit()
    except Exception as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

update_database(config.db)
