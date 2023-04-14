test_mode = False

# try:
#     import RPi.GPIO as GPIO
# except ImportError:
#     print("Entering test mode")
#     test_mode = True

from data_manager import DataManager
from sensor import BME280
from time import sleep


import json





class ControlModule:
    '''
    class to control multiple elements of the initial sensor information

    expects:
    heat_threshold: touple: low value to ON relay, high value to OFF relay
    cold_threshold: touple: low value to OFF relay, high value to ON relay
    humidity_threshold: touple: low value to ON relay, high value to OFF relay
    heater,cooler,hum,extrn,_relay_pin: GPIO number for signal for relay comms

    Order of operations:

    1)Refreshes current sensor values
    2)checks current values vs ON/OFF thresholds
        2.5) if outside threshold values, checks alarms (which can write to alarms.csv)
    3)writes to raw.csv to be processed by data-dir scripts
    
    '''
    def __init__(self, settings = "controller/settings.json", heat_pin = 0, ac_pin = 0, hum_pin = 0, fan_pin = 0, light_pin = 0):


        self.sensor = BME280() #Reach sensor
        self.data_manager = DataManager() #What controls writing and saving the data

        with open(settings, 'r') as file:
            data = json.load(file)
        # Extract the settings from the JSON data
        self.settings = data['Thresholds']
        print(self.settings)
        #Written as follows:
        # "Thresholds": {"LL":#, "HON":#, "HOFF":#, "CON": #, "COFF" : #, "HH":#, "HUMON": #, "HUMOFF":#}


        # self.heat_threshold = heat_threshold #set thresholds for low (on) and high (off) for relays
        # self.cold_threshold = cold_threshold
        # self.humidity_threshold = humidity_threshold

        # set the GPIO pins to use
        self.heat_pin = heat_pin
        self.ac_pin = ac_pin
        self.hum_pin = hum_pin
        self.fan_pin = fan_pin
        self.light_pin = light_pin
        # set the pins as output and turn them off
        # GPIO.setup(self.heat_pin, GPIO.OUT)
        # GPIO.setup(self.ac_pin, GPIO.OUT)
        # GPIO.setup(self.hum_pin, GPIO.OUT)
        # GPIO.setup(self.fan_pin, GPIO.OUT)
        # GPIO.setup(self.light_pin, GPIO.OUT)
        # GPIO.output(self.heat_pin, False)
        # GPIO.output(self.ac_pin, False)
        # GPIO.output(self.hum_pin, False)
        # GPIO.output(self.fan_pin, False)
        # GPIO.output(self.light_pin, False)

        #Should be immediately changed by sensor updates
        self.current_temp = 0
        self.current_hum = 0

    def update_readings_from_sensor(self):
        '''self.current_temp, self.current_hum = self.sensor.update_readings()'''
        self.current_temp, self.current_hum = self.sensor.update_readings()

    def check_vs_thresholds(self):
        '''
        do stuff to check allowed thresholds 
        turn off/on relays when needed
        if beyond accepted thresholds, check vs alarm values
        '''
        pass
        # turn heater on if temp is too low
        # if self.current_temp <= self.heat_threshold[0]:
        #     GPIO.output(self.heat_pin, True)
        #     GPIO.output(self.ac_pin, False)
        # # turn heater off if temp is good
        # if self.current_temp >= self.heat_threshold[1]:
        #     GPIO.output(self.heat_pin, False)
        # # turn ac on if temp is too high
        # if self.current_temp >= self.cold_threshold[0]:
        #     GPIO.output(self.ac_pin, True)
        #     GPIO.output(self.heat_pin, False)
        # # turn ac off if temp is good
        # if self.current_temp <= self.cold_threshold[1]:
        #     GPIO.output(self.ac_pin, False)
        # # turn humidifier on if humidity is too low
        # if self.current_hum <= self.humidity_threshold[0]:
        #     GPIO.output(self.hum_pin, True)
        # # turn humidifier off if humidity is good
        # if self.current_hum >= self.humidity_threshold[1]:
        #     GPIO.output(self.hum_pin, False)
        # # testing code
        # while True:
        #     GPIO.output(self.heat_pin, True)
        #     sleep(5)
        #     GPIO.output(self.heat_pin, False)

    def record(self):
        self.data_manager.update_data(self.current_temp, self.current_hum)
        self.data_manager.record_data()
        
    def control_relay(self):
        # temperature, humidity = self.read_sensor_data()
        # if temperature >= self.temperature_threshold or humidity >= self.humidity_threshold:
        #     if not self.is_relay_on:
        #         GPIO.output(self.relay_pin, GPIO.HIGH)
        #         self.is_relay_on = True
        # else:
        #     if self.is_relay_on:
        #         GPIO.output(self.relay_pin, GPIO.LOW)
        #         self.is_relay_on = False
        pass



controller = ControlModule()
controller.update_readings_from_sensor()
controller.record()