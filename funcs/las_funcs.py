from RPi import GPIO as GPIO

from functions import LAS_SETTINGS


def initialize_lasers():
    for pin in LAS_SETTINGS['laserPins']:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)


def turn_on_laser(laser):
    for las in LAS_SETTINGS['laserPins']:
        GPIO.output(las, False)

    GPIO.output(LAS_SETTINGS['laserPins'][laser], True)


def laser_count_generator():
    def init():
        return 0

    num = init()
    while True:
        val = (yield num % 4)
        if val == 'restart':
            i = init()
        else:
            num += 1


def turn_off_all_lasers():
    active_pins = []
    for i in range(1, 41):
        if i not in [1, 2, 4, 6, 9, 14, 17, 20, 25, 27, 28, 30, 34, 39]:
            if GPIO.gpio_function(i) is not -1:
                active_pins.append(i)
    cleanup_pins = [pin for pin in active_pins if pin not in [10, 13, 15, 16]]
    GPIO.cleanup(cleanup_pins)
