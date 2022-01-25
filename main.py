# TODO:
# dwa dźwięki na raz (numer_dźwięku)
# która opcja się wyświetla w song menu
# nauka
# bluetooth

import time
from consts import *
from database import *

import RPi.GPIO as GPIO
from RPLCD import CharLCD
from consts import *

import Adafruit_MPR121.MPR121 as MPR121

DEBUG = 1  # enable console output

current_menu = 0  # 0 - main menu, 1 - songs menu (to play), 2 - songs menu (to learn)
conn = None  # db connection
max_song_id = None
cap = MPR121.MPR121()
option_chosen = 0


#
# --------------------------------EMBEEDED---------------------------------------

def init():
    """"Initialize GPIO pins and all devices"""
    global cap

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in pins_out.keys():
        GPIO.setup(pins_out[pin], GPIO.OUT)
    for button in buttons.keys():
        GPIO.setup(buttons[button], GPIO.IN,
                   pull_up_down=GPIO.PUD_UP)  # an input pin, set initial value to be pulled low (off)

    GPIO.add_event_detect(buttons["up"], GPIO.FALLING, callback=on_click_button_up, bouncetime=1500)  # Setup event on rising edge
    GPIO.add_event_detect(buttons["down"], GPIO.FALLING, callback=on_click_button_down, bouncetime=1500)
    GPIO.add_event_detect(buttons["ok"], GPIO.FALLING, callback=on_click_button_ok, bouncetime=1500)

    # buzzer = GPIO.PWM(pins_out["BUZZER"], 440)
    # buzzer.start(50)
    if DEBUG: print("Initialization completed successfully")

    if not cap.begin():
        print('Error initializing MPR121.  Check your wiring!')
        sys.exit(1)
    else:
        print('MPR121 Initialized')


def play_tone(frequency, duration):
    """Play tone on buzzer"""
    print("play_tone: ", frequency, "duration: ", duration)
    buzzer = pins_out["BUZZER"]
    halve_wave_time = 1 / (frequency * 2)
    waves = int(duration * frequency)
    for i in range(waves):
        GPIO.output(buzzer, True)
        time.sleep(halve_wave_time)
        GPIO.output(buzzer, False)
        time.sleep(halve_wave_time)


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
    play_tone(sounds[note], beat)  # TODO: play 2 sounds

    if DEBUG: print("playing sound: ", note)
    time.sleep(beat * 0.1)
    # be_quiet()

    light_off()


def show_text_lcd(text: str, line=0):
    """Show text on lcd (accepts \n\r)"""

    lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=pins_out["LCD_RS"], pin_e=pins_out["LCD_E"], pins_data=[pins_out["LCD_D4"], pins_out["LCD_D5"], pins_out["LCD_D6"], pins_out["LCD_D7"]])

    lcd.cursor_pos = (line, 0)
    lcd.write_string(text)
    if DEBUG: print("ON LCD:", text)


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


def check_keys(freeplay: False, learnsong: False, song_id: None):
    global cap
    if DEBUG: print("Checking keys...")

    if learnsong:
        song = get_song(song_id)
        light_diode(diodes[song[note_counter][0]])
        is_lighted = True

    note_counter = 0

    # read adafruit pins (which of x and y were pressed)
    last_touched = cap.touched()
    while True:

        for el in [[0, 1], [0, 0], [1, 0], [1, 1]]:
            A = el[0]
            B = el[1]

            # read a and b (which of the fours were pressed 00/01/10/11, format: AB)
            GPIO.output(pins_out["ADDR_A"], A)
            GPIO.output(pins_out["ADDR_B"], B)

            # read which multiplexer and if x or y were activated
            current_touched = cap.touched()
            # print(current_touched)
            for i in range(12):
                pin_bit = 1 << i
                if current_touched & pin_bit and not last_touched & pin_bit:
                    key = key_muxes[i] + str(A) + str(B)
                    print(f'Touched! {key_muxes[i]}{A}{B} {piano_keys[key]}')

                    # light_diode(diodes[piano_keys[key]])

                    # free play mode
                    if freeplay:
                        play_sound(piano_keys[key], 0.1)

                    # learn song mode
                    if learnsong and note_counter < len(song):

                        # if diode is lighted and user pressed correct key, play sound and light off diode
                        if song[note_counter][0] == piano_keys[key] and is_lighted:
                            play_tone(sounds[piano_keys[key]], 0.1)
                            light_off()
                            note_counter += 1
                            is_lighted = False

                        if note_counter == len(song): return

                        # light diode for user to press key
                        if not is_lighted:
                            light_diode(diodes[song[note_counter][0]])
                            is_lighted = True



                # if not current_touched & pin_bit and last_touched & pin_bit:
                #     light_off()

            last_touched = current_touched
            time.sleep(0.025)


# ----------------------------------THE VIP FUNCTIONS-----------------------------------------------------------

def free_play():
    """Check which key is pressed and play it"""
    print("free_play")
    check_keys(freeplay=True, learnsong=False, song_id=None)


def play_song(song_id):
    """Play song and light diodes without user's interactions"""
    print("play_song")
    song = get_song(song_id)
    print("got song")

    for note in song:
        print(note)
        play_sound(*note)


def learn_song(song_id):
    """Light diodes only for sounds which should be played in right order"""
    print("learn_song")
    check_keys(freeplay=False, learnsong=True, song_id=song_id)


def shutdown_piano():
    """"Clean and exit"""
    show_text_lcd("Do zobaczenia!")
    GPIO.cleanup()
    conn.close()
    time.sleep(2)
    exit(0)
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
    options = ["Graj sam", "Odtworz utwor", "Naucz sie grac", "Wyjscie"]
    option_chosen = option_chosen % 4

    show_text_lcd("<" + options[option_chosen] + ">\r\n" + options[(option_chosen + 1) % 4])


def refresh_songs_menu():
    """ Select songs from Songs database """
    global conn
    global option_chosen
    global max_song_id
    print("refresh_songs_menu")
    option_chosen = option_chosen % (max_song_id + 2)
    next_option = (option_chosen + 1) % (max_song_id + 2)

    cursor = conn.cursor()
    if next_option == max_song_id + 1:
        cursor.execute(f'SELECT title FROM Songs WHERE id IN ({option_chosen})')
        names = [cursor.fetchone()[0], "powrot"]
    elif option_chosen == max_song_id + 1:
        cursor.execute(f'SELECT title FROM Songs WHERE id IN ({next_option})')
        names = ["powrot", cursor.fetchone()[0]]
    else:
        cursor.execute(f'SELECT title FROM Songs WHERE id IN ({option_chosen}, {next_option})')
        names = cursor.fetchall()
        names = [names[0][0], names[1][0]]

    if len(names[0]) > 14: names[0] = names[0][:14]
    if len(names[1]) > 16: names[1] = names[1][:16]
    print(names)

    # dodaj exit jako ostatnią funkcję do names

    show_text_lcd(f"<{names[0]}>\r\n{names[1]}")


def choose_option_main_menu():
    global current_menu
    global option_chosen
    print(f"choose_option_main_menu {option_chosen}")
    if option_chosen == 0:
        free_play()

    elif option_chosen == 1:
        option_chosen = 0
        current_menu = 1
        refresh_songs_menu()

    elif option_chosen == 2:
        option_chosen = 0
        current_menu = 2
        refresh_songs_menu()
    else:
        shutdown_piano()


def choose_option_songs_menu():
    global current_menu
    print("choose_option_songs_menu", option_chosen)
    if current_menu == 1:
        if option_chosen == max_song_id + 1:
            current_menu = 0
            refresh_main_menu()
        else: play_song(option_chosen)
    elif current_menu == 2:
        if option_chosen == max_song_id + 1:
            current_menu = 0
            refresh_main_menu()
        else: learn_song(option_chosen)


# ---------------------------

def main():
    global conn
    global max_song_id
    init()
    show_text_lcd("Dzien dobry!")

    # wave on diodes
    # for diode in diodes.values():
    #     light_diode(diode)
    #     time.sleep(0.05)
    # light_off()
    # for diode in list(diodes.values())[::-1]:
    #     light_diode(diode)
    #     time.sleep(0.05)
    light_off()

    conn = create_connection("piano.db")
    cur = conn.cursor()

    if conn is None:
        show_text_lcd("Brak bazy piosenek")
        free_play()
    else:
        with conn:
            max_song_id = get_max_song_id(conn)
            refresh_main_menu()
            while (True):
                pass


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
