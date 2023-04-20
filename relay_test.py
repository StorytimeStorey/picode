import RPi.GPIO as GPIO
from time import sleep
import json
GPIO.setmode(GPIO.board)
if __name__ == '__main__':
    # open settings json
    with open('picode/controller/settings.json', 'r') as file:
        data = json.load(file)
        pins = data['GPIO_Pins']
    # set variables for each pin
    heat_pin = pins['heat_pin']
    ac_pin = pins['ac_pin']
    hum_pin = pins['hum_pin']
    fan_pin = pins['fan_pin']
    light_pin = pins['light_pin']
    # tests each relay, relays should turn on for 5 seconds and then shut off
    for key, value in list(pins.items()):
        if value:
            current_pin = value
            print(current_pin)
            print(f"testing {key} at pin {value}")
            GPIO.setup(current_pin, GPIO.OUT)
            GPIO.output(current_pin, False)
            sleep(5)
            GPIO.output(current_pin, True)
        else:
            print(f"{key} is not set up")

    GPIO.cleanup()

