# import time
# import board
# from adafruit_bme280 import basic as adafruit_bme280

# # Create sensor object, using the board's default I2C bus.
# i2c = board.I2C()  # uses board.SCL and board.SDA
# # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
# bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# # OR create sensor object, using the board's default SPI bus.
# # spi = board.SPI()
# # bme_cs = digitalio.DigitalInOut(board.D10)
# # bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# # change this to match the location's pressure (hPa) at sea level
# bme280.sea_level_pressure = 1013.25

# while True:
#     print("\nTemperature: %0.1f C" % bme280.temperature)
#     print("Humidity: %0.1f %%" % bme280.relative_humidity)
#     print("Pressure: %0.1f hPa" % bme280.pressure)
#     print("Altitude = %0.2f meters" % bme280.altitude)
#     time.sleep(2)

import time
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280

print("""all-values.py - Read temperature, pressure, and humidity
Press Ctrl+C to exit!
""")

# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

while True:
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperature, pressure, humidity))
    time.sleep(1)