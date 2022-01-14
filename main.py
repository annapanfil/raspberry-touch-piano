# TODO:
# - dwa dźwięki na raz (numer_dźwięku)
# klawisze

import time
from consts import *
# from low_level import *
from database import *

import RPi.GPIO as GPIO
from RPLCD import CharLCD
from consts import *

DEBUG = 1  # enable console output

buzzer = None
current_menu = 0  # 0 - main menu, 1 - songs menu (to play), 2 - songs menu (to learn)
conn = None  # db connection
max_song_id = None
cap = MPR121.MPR121()


# --------------------------------EMBEEDED---------------------------------------

def init():
    """"Initialize GPIO pins and all devices"""
    # global buzzer

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in pins_out.keys():
        GPIO.setup(pins_out[pin], GPIO.OUT)
    for button in buttons.keys():
        GPIO.setup(buttons[button], GPIO.IN,
                   pull_up_down=GPIO.PUD_UP)  # an input pin, set initial value to be pulled low (off)

    GPIO.add_event_detect(buttons["up"], GPIO.FALLING, callback=on_click_button_up)  # Setup event on rising edge
    GPIO.add_event_detect(buttons["down"], GPIO.FALLING, callback=on_click_button_down)
    GPIO.add_event_detect(buttons["ok"], GPIO.FALLING, callback=on_click_button_ok)

    # buzzer = GPIO.PWM(pins_out["BUZZER"], 440)
    # buzzer.start(50)
    if DEBUG: print("Initialization completed successfully")


def play_tone(frequency):
    """Play tone on buzzer"""
    print("play_tone", frequency)
    # global buzzer
    # buzzer.duty_u16(1000)
    # buzzer.freq(frequency)


def be_quiet():
    """Turn the buzzer off"""
    print("quiet")
    # global buzzer
    # buzzer.duty_u16(0)


def light_diode(addr: list):
    if DEBUG: print("diode", addr, "is on")
    if addr[0] == 'X':
        GPIO.output(pins_out["MAIN_MUX_Y"], GPIO.LOW)
        GPIO.output(pins_out["MAIN_MUX_X"], GPIO.HIGH)
    elif addr[0] == 'Y':
        GPIO.output(pins_out["MAIN_MUX_Y"], GPIO.HIGH)
        GPIO.output(pins_out["MAIN_MUX_X"], GPIO.LOW)

    GPIO.output(pins_out["MAIN_MUX_ADDR_A"], addr[1])
    GPIO.output(pins_out["MAIN_MUX_ADDR_B"], addr[2])
    GPIO.output(pins_out["ALL_MUX_ADDR_A"], addr[3])
    GPIO.output(pins_out["ALL_MUX_ADDR_B"], addr[4])


def light_off():
    """Turn off all diodes"""

    if DEBUG: print("diodes are off")
    GPIO.output(pins_out["MAIN_MUX_Y"], GPIO.LOW)
    GPIO.output(pins_out["MAIN_MUX_X"], GPIO.LOW)


def play_sound(note: str, beat=0.01):
    """Play tone on the buzzer and light the diode for certain time"""

    light_diode(diodes[note])
    play_tone(sounds[note])  # TODO: play 2 sounds
    if DEBUG: print("playing sound: ", note)
    time.sleep(beat * 0.13)
    be_quiet()
    light_off()


def show_text_lcd(text: str, line=1):
    """Show text on lcd (accepts \n\r)"""

    lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=pins_out["LCD_RS"], pin_e=pins_out["LCD_E"],
                  pins_data=[pins_out["LCD_D4"], pins_out["LCD_D5"], pins_out["LCD_D6"], pins_out["LCD_D7"]])

    lcd.cursor_pos = (line, 0)
    lcd.write_string(text)
    if DEBUG: print("ON LCD:", text)


def get_key():
    # TODO: check on gpio

    # return "C1"
    return None


# ----------------------------------- HELPFUL ----------------------------------

def on_click_button_up(arg):
    global option_chosen
    if DEBUG: print("Button UP pressed")
    option_chosen -= 1
    refresh_menu()


def on_click_button_down(arg):
    global option_chosen
    if DEBUG: print("Button DOWN pressed")
    option_chosen += 1
    refresh_menu()


def on_click_button_ok(arg):
    if DEBUG: print("Button OK pressed")
    if current_menu == 0:
        choose_option_main_menu()
    elif current_menu in (1, 2):
        choose_option_songs_menu()


def check_keys():
    # if DEBUG: print("Checking keys...")
    # for key in piano_keys.keys():
    #     if get_key(key):
    #         return key
    # return None

    last_touched = cap.touched()
    while True:

        current_touched = cap.touched()
        for i in range(12):
            pin_bit = 1 << i
            if current_touched & pin_bit and not last_touched & pin_bit:
                print('{0} touched!'.format(i))

            if not current_touched & pin_bit and last_touched & pin_bit:
                print('{0} released!'.format(i))

        last_touched = current_touched
        time.sleep(0.1)

# ----------------------------------THE VIP FUNCTIONS-----------------------------------------------------------

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
    # TODO: shutdown pi


# ------------------------------------MENU(S)----------------------------------------------------
def refresh_menu():
    if current_menu == 0:
        refresh_main_menu()
    elif current_menu == 1:
        refresh_songs_menu()
    elif current_menu == 2:
        refresh_songs_menu()


def refresh_main_menu():
    """Wyświetl opcje i czekaj na naciśnięcie przycisku"""
    global option_chosen
    options = ["Graj sam", "Odtworz melodie", "Naucz sie grac", "Wyjscie"]
    option_chosen = option_chosen % 4

    show_text_lcd("< " + options[option_chosen] + " >")
    show_text_lcd(options[(option_chosen + 1) % 4])


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
    if option_chosen == 0:
        free_play()

    elif option_chosen == 1:
        current_menu = 1

    elif option_chosen == 2:
        current_menu = 2
    else:
        shutdown_piano()


def choose_option_songs_menu():
    if current_menu == 1:
        play_song(option_chosen)
    elif current_menu == 2:
        learn_song(option_chosen)


# ------------------------------------------------------------------------------


# ---------------------------

def main():
    init()
    show_text_lcd("Dzien dobry!")

    # wave on diodes
    for diode in diodes.values():
        light_diode(diode)
        time.sleep(0.1)
    light_off()

    conn = create_connection("piano.db")
    if conn == None:
        show_text_lcd("Brak bazy piosenek")
        free_play()
    else:
        with conn:
            refresh_main_menu()
            while (True):
                pass


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

