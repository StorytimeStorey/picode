import RPi.GPIO as GPIO
from time import sleep
heat_pin = 16
GPIO.setmode(heat_pin, GPIO.OUT)
GPIO.output(heat_pin, False)

while True:
    GPIO.output(heat_pin, True)
    sleep(5)
    GPIO.output(heat_pin, False)