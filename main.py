#TODO:
# - dwa dźwięki na raz (numer_dźwięku)
# klawisze, LCD

import time
from consts import *
from low_level import *
from database import *

buzzer = None
option_chosen = 0
current_menu = 0  # 0 - main menu, 1 - songs menu (to play), 2 - songs menu (to learn)
conn = None # db connection
max_song_id = None

#----------------------------------THE VIP FUNCTIONS-----------------------------------------------------------

def free_play():
    """Check which key is pressed and play it"""

    while True:
        note = check_keys()
        play_sound(note)


def play_song(song_id):
    """Play song and light diodes without user's interactions"""
    song = get_song(song_id)

    for note in song:
        play_sound(*note)


def learn_song(song_id):
    """Light diodes only for sounds which should be played in right order"""

    song = get_song(song_id)

    for note in song:
        light_diode(diodes[note[0]])
        while check_keys() != note[0]: pass
        play_sound(*note)
        light_off()


def shutdown_piano():
    """"Clean and exit"""
    GPIO.cleanup()
    conn.close()
    show_text_lcd("Goodbye!")
    time.sleep(2)
    #TODO: shutdown pi


# ------------------------------------MENU(S)----------------------------------------------------
def refresh_menu():
    if current_menu == 0: refresh_main_menu()
    elif current_menu == 1: refresh_songs_menu()
    elif current_menu == 2: refresh_songs_menu()


def refresh_main_menu(conn):
    """Wyświetl opcje i czekaj na naciśnięcie przycisku"""
    global option_chosen
    options = ["Graj sam", "Odtwórz melodię", "Naucz się grać", "Wyjście"]
    option_chosen = option_chosen % 4

    show_text_lcd("< " + options[option_chosen] + " >")
    show_text_lcd(options[(option_chosen+1)%4])


def refresh_songs_menu(conn):
    """ Select songs from Songs database """

    global option_chosen
    option_chosen = option_chosen % max_song_id
    next_option = (option_chosen + 1) % max_song_id

    cursor = conn.cursor()
    cursor.execute(f'SELECT title FROM Songs WHERE id IN ({option_chosen}, {next_option})')
    names = cursor.fetchall()

    show_text_lcd(names[0])
    show_text_lcd(names[1])


def choose_option_main_menu():
    if option_chosen == 0: free_play()

    elif option_chosen == 1:
        current_menu = 1

    elif option_chosen == 2:
        current_menu = 2
    else: shutdown_piano()


def choose_option_songs_menu():
    if current_menu == 1:
        play_song(option_chosen)
    elif current_menu == 2:
        learn_song(option_chosen)

#------------------------------------------------------------------------------

def main():
    show_text_lcd("Dzien dobry!")
    #TODO: light all diodes in order
    time.sleep(2)
    conn = create_connection("piano.db")
    if conn == None:
        show_text_lcd("Brak bazy piosenek")
        free_play()
    else:
        with conn:
            refresh_main_menu()

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
