import RPi.GPIO as GPIO

# set the GPIO pins to use
pin1 = 4
pin2 = 5
# pin2 = 6
# pin3 = 27

GPIO.setmode(GPIO.BOARD)

def initialize_pins():
    # initilaize the pins as being off
    GPIO.setup(pin1, False)
    GPIO.setup(pin2, False)

