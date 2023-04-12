import RPi.GPIO as GPIO
from time import sleep
heat_pin = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(heat_pin, GPIO.OUT)
GPIO.output(heat_pin, False)
try:
    while True:
        GPIO.output(heat_pin, True)
        sleep(15)
        GPIO.output(heat_pin, False)
        sleep(15)
except KeyboardInterrupt:
    GPIO.cleanup()