#TODO: 
# - dwa dźwięki na raz (numer_dźwięku)
# - baza danych
# - niskopoziomowe
# - przerwanie danego trybu i powrót do menu


import RPi.GPIO as GPIO
import time
import sqlite3
from sqlite3 import Error
from consts import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Buzz = None
db_connection = None

#--------------------------------EMBEEDED XD------------------------------------------------------
def init():
    global Buzz
    for pin in pins.keys():
        GPIO.setup(pins["pin"], GPIO.OUT)

    Buzz = GPIO.PWM(pins["BUZZER"], 440)
    Buzz.start(50)


def light_diode(addr: list):
    GPIO.output(pins["MAIN_MUX_Y"], GPIO.HIGH)
    GPIO.output(pins["MAIN_MUX_X"], GPIO.HIGH)
    GPIO.output(pins["MAIN_MUX_ADDR_A"], addr[0])
    GPIO.output(pins["MAIN_MUX_ADDR_B"], addr[1])
    GPIO.output(pins["FIRST_MUX_ADDR_A"], addr[2])
    GPIO.output(pins["FIRST_MUX_ADDR_B"], addr[3])


def light_off():
    GPIO.output(pins["MAIN_MUX_Y"], GPIO.LOW)
    GPIO.output(pins["MAIN_MUX_X"], GPIO.LOW)


def play_sound(note: str, beat = 0.01):
    global Buzz
    light_diode(diodes[note])
    Buzz.ChangeFrequency(sounds[note]) #TODO: play 2 sounds
    time.sleep(beat*0.13)
    #TODO: buzzer off
    light_off()


def get_button(button: str):
    #TODO: check on gpio
    pass


def show_text_lcd(text: str):
    print(text)
    #TODO: show on LCD
    pass


def get_key():
    #TODO: check on gpio
    pass

# ----------------------------------- HELPFUL -----------------------------------------------------------

def check_buttons():
    for button in buttons.keys():
        if get_button(button):
            return button
    return None


def check_keys():
    for key in piano_keys.keys():
        if get_key(key):
            return key
    return None


#----------------------------------THE VIP FUNCTIONS-----------------------------------------------------------

def free_play():
    """check which key is pressed and play it"""
    while True:
        note = check_keys()
        play_sound(note)
    

def play_song(song_id):
    """Play song and light diodes without user's interactions"""
    #TODO: song = wyciągnij info z bazy Dzwieki_w_piosenkach (nazwa, długość)
    for note in song:
        play_sound(note)


def learn_song(song_id):
    """light diodes only for sounds which should be played in right order"""
    #TODO: song = wyciągnij info z bazy Dzwieki_w_piosenkach note = (nazwa, długość)

    for note in song:
        light_diode(diodes[note[0]])
        while check_keys() != note[0]: pass
        play_sound(*note)
        light_off()


def shutdown_piano():
    """"Clean and exit"""
    #TODO: close GPIO
    show_text_lcd("Goodbye!")
    time.sleep(2)
    #TODO: shutdown pi
    pass


# ------------------------------------MENU(S)----------------------------------------------------

def show_songs():
    #TODO: show which songs are in Piosenki database (id, nazwa)
    options = []
    names = []
    option_now = 0
    
    while True:
        
        songs_size = len(options)

        print(names[option_now])
        print(names[(option_now+1)%songs_size])
        
        button = None
        while not button:
            button = check_buttons()

        if button == "up": option_now += 1
        elif button == "down": option_now -= 1
        elif button == "ok": 
            return options[option_now] #song_id


def show_menu():
    """Wyświetl opcje i czekaj na naciśnięcie przycisku"""
    
    options = ["Graj sam", "Odtwórz melodię", "Naucz się grać", "Wyjście"]
    option_now = 0

    while True:
        
        show_text_lcd("< " + options[option_now] + " >")
        show_text_lcd(options[(option_now+1)%4])
        
        button = None
        while not button:
            button = check_buttons()

        if button == "up": option_now += 1
        elif button == "down": option_now -= 1
        elif button == "ok": 
            if option_now == 0: free_play()

            elif option_now == 1: 
                song_id = show_songs()
                play_song(song_id)

            elif option_now == 2: 
                song_id = show_songs()
                learn_song(song_id)

            else: shutdown_piano()



if __name__ == "__main__":
    show_text_lcd("Dzien dobry!")
    time.sleep(2)
    #TODO: light all diodes in order
    show_menu()

