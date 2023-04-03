import random
import time

test_mode = False
try:  #test to see if sensor is connected
    from bmp280 import BMP280
    print("Sensor bmp280 found")
except ImportError: #if not, enter test mode
    print("Sensor not found, entering test mode")
    test_mode = True

try:
    from smbus2 import SMBus
except ImportError:
    try:
        from smbus import SMBus
    except ImportError: #another check for test mode
        print("Entering test mode, all data saved will go to data/test")
        test_mode = True

class Sensor:
    '''
    Code for connecting to the specific sensor
    Currently BMP280, would eventually like to get a BME280.

    If sensor isn't found, enters "test mode" which sets everything to chosen values and saves random info to a test csv
    sets self.test_mode = True, which should cascade testing environment changes
    '''
    def __init__(self, temp_low = 55, temp_high = 75, hum_low = 82, hum_high = 99):
        if not test_mode:
            self.bus = SMBus(1)
            self.bmp280 = BMP280(i2c_dev=self.bus)
            self.temperature = 0
            self.pressure = 0


        else: #CODE FOR TESTING ENVIRONMENT
            self.test_mode = True
            print("current_sensor.py is in test mode")
            self.temperature = 0
            self.pressure = 0   
            self.temp_low = temp_low
            self.temp_high = temp_high
            self.hum_low = hum_low
            self.hum_high = hum_high


    def update_readings(self):

        if not self.test_mode:
            self.temperature = round(self.bmp280.get_temperature() * 9/5 + 32, 1)
            self.pressure = round(self.bmp280.get_pressure(),2)

        else: #CODE FOR TESTING ENVIRONMENT
            self.temperature = round(random.uniform(self.temp_low, self.temp_high), 1)
            self.pressure = round(random.uniform(self.hum_low, self.hum_high), 2)