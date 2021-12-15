import RPi.GPIO as GPIO
import time
from consts import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def init():
    for pin in pins.keys():
        GPIO.setup(pins["pin"], GPIO.OUT)

    Buzz = GPIO.PWM(BUZZER, 440)
    Buzz.start(50)

def light_by_addr(addr: list):
    GPIO.output(MAIN_MUX_Y, GPIO.HIGH)
    GPIO.output(MAIN_MUX_X, GPIO.HIGH)
    GPIO.output(MAIN_MUX_ADDR_A, addr[0])
    GPIO.output(MAIN_MUX_ADDR_B, addr[1])
    GPIO.output(FIRST_MUX_ADDR_A, addr[2])
    GPIO.output(FIRST_MUX_ADDR_B, addr[3])

def light_off():
    GPIO.output(MAIN_MUX_Y, GPIO.LOW)
    GPIO.output(MAIN_MUX_X, GPIO.LOW)

def print_text():
    pass

def play_sound(note: str, beat:int):
    Buzz.ChangeFrequency(sounds[sound])
    time.sleep(beat*0.13)
    light_by_addr(diodes[note])

def play_song():
    # song = wyciągnij info z bazy
    for note in song:
        play_sound(note)

def get_button():
    pass

def show_menu():
    # titles = wyciągnij info z bazy
    



if __name__ == "__main__":
    print_text("Dzien dobry!")
    while BUTTON_OK == 0:
        show_menu()
        get_button()
