
import time
from bmp280 import BMP280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

class Sensor:
    '''
    Code for connecting to the specific sensor
    Currently BMP280, would eventually like to get a BME280.

    '''
    def __init__(self):
        self.bus = SMBus(1)
        self.bmp280 = BMP280(i2c_dev=self.bus)
        self.temperature = 0
        self.pressure = 0

    def update_readings(self):
        self.temperature = round(self.bmp280.get_temperature(), 1)
        self.pressure = round(self.bmp280.get_pressure(),2)
    
    # update_readings(self)