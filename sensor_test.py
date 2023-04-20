import random

test_mode = False
try:
    import board
    from adafruit_bme280 import basic as adafruit_bme280
    print("Sensor bme280 found")
except ImportError: 
    print("Sensor not found, entering test mode")
    test_mode = True



class Sensor:
    '''
    Code for connecting to the BME280.

    If sensor isn't found, enters "test mode" which sets everything to chosen values and saves random info to a test csv
    sets self.test_mode = True, which should cascade testing environment changes

    Initial variables:
        i2c - gets the I2C to use when activating the BME280
        bmp280 - initializes the BME280 sensor
        temperature - the current temperature of the environment
        humidity - the current humidity of the environment
        test_mode - True/False boolean to determine whether to run real or testing code
    '''
    def __init__(self, temp_low = 55, temp_high = 75, hum_low = 82, hum_high = 99,):
        if not test_mode:
            self.i2c = board.I2C()  # uses board.SCL and board.SDA
            self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.i2c)
            self.temperature = 0
            self.humidity = 0
            self.test_mode = test_mode


        else: #CODE FOR TESTING ENVIRONMENT
            self.test_mode = test_mode
            print("current_sensor.py is in test mode")
            self.temperature = 0
            self.humidity = 0   
            self.temp_low = temp_low
            self.temp_high = temp_high
            self.hum_low = hum_low
            self.hum_high = hum_high


    def update_readings(self):
        '''
        Updates the current temperature and humidity levels
        '''
        if not self.test_mode:
            self.temperature = round(self.bme280.temperature * 9/5 + 32, 1)
            self.humidity = round(self.bme280.relative_humidity ,2)

        else: #CODE FOR TESTING ENVIRONMENT
            self.temperature = round(random.uniform(self.temp_low, self.temp_high), 1)
            self.humidity = round(random.uniform(self.hum_low, self.hum_high), 2)


if __name__ == '__main__':
    test_sensor = Sensor()
    try:
        for i in range(30):
            test_sensor.update_readings()
            print(test_sensor.temperature)
            print(test_sensor.humidity)
        print('testing complete')
    except KeyboardInterrupt:
        print('testing interuppted by user input')