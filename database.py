import sqlite3
from sqlite3 import Error

# ------------------------ DATABASE---------------------------------------------

def create_connection(db_file):
    """Connect to database"""

    global conn
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        print("Connected to database")
        return conn
    except Error as e:
        print(e)
        show_text_lcd(e)
        return None


def get_max_song_id(connection):
    """How many songs in the database"""

    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Songs")
    max_song_id = cursor.fetchone()[0] - 1
    print("max_song_id", max_song_id)
    cursor.close()
    return max_song_id


def get_song(song_id):
    """Get all sounds in the song"""

    global conn
    print("get_song")
    cursor = conn.cursor()
    print("cursor created")
    cursor.execute(f'SELECT sound_name, sound_length FROM Sounds_in_songs WHERE song_id = {song_id} ORDER BY sound_number')
    song = cursor.fetchall()
    cursor.close()
    return song
