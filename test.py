import sqlite3
from sqlite3 import Error
from consts import *


def create_connection(db_file):
    try:
        db_connection = sqlite3.connect(db_file)
        print("Connected to database")
        return db_connection
    except Error as e:
        print(e)
        show_text_lcd(e)
        return None


def play_song(song_id, conn):
    """Play song and light diodes without user's interactions"""
    cursor = conn.cursor()
    cursor.execute(f'SELECT sound_name, sound_length FROM Sounds_in_songs WHERE song_id = {song_id} ORDER BY sound_number')
    song = cursor.fetchall()
    print(song)
    
    #TODO: song = wyciągnij info z bazy Dzwieki_w_piosenkach (nazwa, długość)
    # for note in song:
    #     play_sound(note)


conn = create_connection("piano.db")
with conn:
    play_song(0, conn)