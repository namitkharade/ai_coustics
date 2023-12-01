import sqlite3
import config

def view_db():
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(config.db)
        cursor = connection.cursor()

        # Execute the SELECT query
        cursor.execute('SELECT * FROM audio_info')

        # Fetch all rows
        rows = cursor.fetchall()

        # Print the result
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        # Close the connection
        if connection:
            connection.close()