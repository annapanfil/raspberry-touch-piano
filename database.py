import sqlite3
from sqlite3 import Error

# ------------------------ DATABASE---------------------------------------------

def create_connection(db_file):
    """Connect to database"""

    global conn
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to database")
        return conn
    except Error as e:
        print(e)
        show_text_lcd(e)
        return None


def get_max_song_id():
    """How many songs in the database"""

    global max_song_id
    cursor = conn.cursor()
    cursor.execute(f'SELECT id FROM songs ORDER BY id LIMIT 1')
    max_song_id = cursor.fetchall()[0][0]
    cursor.close()
    return max_song_id


def get_song(song_id):
    """Get all sounds in the song"""

    global conn
    cursor = conn.cursor()
    cursor.execute(f'SELECT sound_name, sound_length FROM Sounds_in_songs WHERE song_id = {song_id} ORDER BY sound_number')
    song = cursor.fetchall()
    cursor.close()
    return song
