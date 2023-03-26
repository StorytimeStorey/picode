
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
        self.bmp280 = BMP280(i2c_dev=bus)
        self.temperature = 0
        self.pressure = 0

    def update_readings(self):
        self.temperature = self.bmp280.get_temperature()
        self.pressure = self.bmp280.get_pressure()
    
    update_readings()