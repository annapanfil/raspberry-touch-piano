#TODO:
# - dwa dźwięki na raz (numer_dźwięku)
# klawisze, LCD

import RPi.GPIO as GPIO
import time
import sqlite3
from sqlite3 import Error
from consts import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buzzer = None
option_chosen = 0
current_menu = 0  # 0 - main menu, 1 - songs menu (to play), 2 - songs menu (to learn)
conn = None # db connection
max_song_id = None

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

#--------------------------------EMBEEDED---------------------------------------

def init():
    """"Initialize GPIO pins and all devices"""

    global buzzer
    for pin in pins_out.keys():
        GPIO.setup(pins_out[pin], GPIO.OUT)
    for button in buttons.keys():
        GPIO.setup(buttons[button], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # an input pin, set initial value to be pulled low (off)

    GPIO.add_event_detect(buttons["up"], GPIO.RISING, callback = on_click_button_up) # Setup event on rising edge
    GPIO.add_event_detect(buttons["down"], GPIO.RISING, callback = on_click_button_down)
    GPIO.add_event_detect(buttons["ok"], GPIO.RISING, callback = on_click_button_ok)

    buzzer = GPIO.PWM(pins_out["BUZZER"], 440)
    buzzer.start(50)


def play_tone(frequency):
    """Play tone on buzzer"""
    global buzzer
    buzzer.duty_u16(1000)
    buzzer.freq(frequency)


def be_quiet():
    """Turn the buzzer off"""
    global buzzer
    buzzer.duty_u16(0)


def light_diode(addr: list):
    GPIO.output(pins_out["MAIN_MUX_Y"], GPIO.HIGH)
    GPIO.output(pins_out["MAIN_MUX_X"], GPIO.HIGH)
    GPIO.output(pins_out["MAIN_MUX_ADDR_A"], addr[0])
    GPIO.output(pins_out["MAIN_MUX_ADDR_B"], addr[1])
    GPIO.output(pins_out["FIRST_MUX_ADDR_A"], addr[2])
    GPIO.output(pins_out["FIRST_MUX_ADDR_B"], addr[3])


def light_off():
    """Turn off all diodes"""

    GPIO.output(pins_out["MAIN_MUX_Y"], GPIO.LOW)
    GPIO.output(pins_out["MAIN_MUX_X"], GPIO.LOW)


def play_sound(note: str, beat = 0.01):
    """Play tone on the buzzer and light the diode for certain time"""
    light_diode(diodes[note])
    play_tone(sounds[note]) #TODO: play 2 sounds
    time.sleep(beat*0.13)
    be_quiet()
    light_off()


def show_text_lcd(text: str):
    print("ON LCD:", text)
    #TODO: show on LCD
    pass


def get_key():
    #TODO: check on gpio
    pass

# ----------------------------------- HELPFUL ----------------------------------

def on_click_button_up():
    global option_chosen
    option_chosen -= 1
    refresh_menu()


def on_click_button_down():
    global option_chosen
    option_chosen += 1
    refresh_menu()


def on_click_button_ok():
    if current_menu == 0:
        choose_option_main_menu()
    elif current_menu in (1,2):
        choose_option_songs_menu()


def check_keys():
    for key in piano_keys.keys():
        if get_key(key):
            return key
    return None


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
