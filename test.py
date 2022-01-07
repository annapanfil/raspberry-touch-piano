"""
przetestowane:
+ get_max_song_id
+ łączenie się z bazą

#TODO:

przygotować funkcje do testowania hardware'u:
- zapalanie i gaszenie diody (to chyba działało)
- show_text_lcd
- zmianę zmiennej przy naciskaniu przycisków up/ down

- play_tone i be_quiet
- play_sound (dioda i buzzer)
- play_song

- logi (printy) w menu

- naciskanie klawiszy (na razie nie ma nic)
- free_play
- learn_song
"""

import sqlite3
from sqlite3 import Error
from consts import *

max_song_id = None

def create_connection(db_file):
    try:
        db_connection = sqlite3.connect(db_file)
        print("Connected to database")
        return db_connection
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

def play_song(song_id, conn):
    """Play song and light diodes without user's interactions"""
    cursor = conn.cursor()
    cursor.execute(f'SELECT sound_name, sound_length FROM Sounds_in_songs WHERE song_id = {song_id} ORDER BY sound_number')
    song = cursor.fetchall()
    print(song)


conn = create_connection("piano.db")
with conn:
    print(get_max_song_id())
    print(max_song_id)
