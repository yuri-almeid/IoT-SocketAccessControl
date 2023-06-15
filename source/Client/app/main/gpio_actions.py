import time

from app import IS_EMBEDDED, PIN_RELAY

if IS_EMBEDDED:
    import RPi.GPIO as gpio


def gpio_setup():
    gpio.setmode(gpio.BOARD)
    gpio.setwarnings(False)

    gpio.setup(PIN_RELAY, gpio.OUT)
    gpio.output(PIN_RELAY, gpio.LOW)


def open_door():
    gpio.output(PIN_RELAY, gpio.HIGH)
    time.sleep(6)
    gpio.output(PIN_RELAY, gpio.LOW)


def unlock_door():
    gpio.output(PIN_RELAY, gpio.HIGH)


def lock_door():
    gpio.output(PIN_RELAY, gpio.LOW)
