test_mode = False
try:
    # import the proper GPIO library for the device
    try:
        import LePotatoPi.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
except ImportError:
    print("Entering test mode")
    test_mode = True

from data_manager import DataManager
from sensor import BME280
from time import sleep
from new_alerts import run_alert
import json

class ControlModule:
    '''
    Class to control multiple elements of the initial sensor information

    Expects:
        thresholds: 
            dict in format: {LL: temp, LHUM: hum, HON: temp, HOFF: temp, CON: temp, COFF: temp, HUMON: hum, HUMOFF: hum, HHUM: hum, HH: temp}
        Pins:
            heat_pin
            ac_pin
            hum_pin
            fan_pin
            light_pin

    Naming Conventions:
        LL - Low-Low, the low temp at which an alert should be sent 
        LHUM - low humidity at which an alert should be sent
        HON - temp at which to turn the heater on
        HOFF - temp at which to turn the heater off
        CON - temp at which to turn the cooler on
        COFF - temp at which to turn the cooler off
        HUMON - humidity level at which to turn the humidifier on
        HUMOFF - humidity level at which to turn the humidifier off
        HHUM - High humidity at which an alert should be sent
        HH - High-High, the high temp at which an alert should be sent

    Order of operations:

    1)Refreshes current sensor values
    2)checks current values vs ON/OFF thresholds
        2.5) if outside threshold values, checks alarms (which can write to alarms.csv)
    3)writes to raw.csv and processed by data_manager scripts
    
    '''
    def __init__(self, settings = "controller/settings.json"):


        self.sensor = BME280() #Reach sensor
        self.data_manager = DataManager() #What controls writing and saving the data

        with open(settings, 'r') as file:
            data = json.load(file)
        # Extract the settings from the JSON data
        self.thresholds = data['Thresholds']
        self.pins = data['GPIO_Pins']
        #Written as follows:
        # "Thresholds": {"LL":#, "HON":#, "HOFF":#, "CON": #, "COFF" : #, "HH":#, "HUMON": #, "HUMOFF":#}
        # "GPIO_Pins":{"heat_pin" : None, "ac_pin" : None, "hum_pin":None, "fan_pin":None,"light_pin":None, "test_mode":False}
        
        # set the GPIO pins to use
        self.heat_pin = self.pins["heat_pin"]
        self.ac_pin = self.pins["ac_pin"]
        self.hum_pin = self.pins["hum_pin"]
        self.fan_pin = self.pins["fan_pin"]
        self.light_pin = self.pins["light_pin"]

        # set the pins as output and turn them off
        for key, value in list(self.pins.items()):
            if value:
                current_pin = eval(f"self.{key}")
                print(f"{key} is at {value}")
                GPIO.setup(current_pin, GPIO.OUT)
                GPIO.output(current_pin, False)
            else:
                print(f"{key} is not set up")

        #Should be immediately changed by sensor updates
        self.current_temp = 0
        self.current_hum = 0

    def update_readings_from_sensor(self):
        '''self.current_temp, self.current_hum = self.sensor.update_readings()'''
        self.current_temp, self.current_hum = self.sensor.update_readings()

    def check_vs_thresholds(self):
        '''
        Determines when and if to turn on or off the heater, ac, and humidifier.
        Also checks if the temps are high or low enough to warrant creating an alert. 
        '''
        pass
        # turn heater on if temp is too low
        if self.current_temp <= self.thresholds['HON'] and self.heat_pin:
            GPIO.output(self.heat_pin, True)
            GPIO.output(self.ac_pin, False)
        # turn heater off if temp is good
        if self.current_temp >= self.thresholds['HOFF'] and self.heat_pin:
            GPIO.output(self.heat_pin, False)
        # turn ac on if temp is too high
        if self.current_temp >= self.thresholds['CON'] and self.ac_pin:
            GPIO.output(self.ac_pin, True)
            GPIO.output(self.heat_pin, False)
        # turn ac off if temp is good
        if self.current_temp <= self.thresholds['COFF'] and self.ac_pin:
            GPIO.output(self.ac_pin, False)
        # turn humidifier on if humidity is too low
        if self.current_hum <= self.thresholds['HUMON'] and self.hum_pin:
            GPIO.output(self.hum_pin, True)
        # turn humidifier off if humidity is good
        if self.current_hum >= self.thresholds['HUMOFF'] and self.hum_pin:
            GPIO.output(self.hum_pin, False)
        # if the temp exceeds the LL or HH values, send an alert
        if self.current_temp <= self.thresholds['LL'] or self.current_temp >= self.thresholds['HH']:
            # determine whether the heater, ac, and humidifier are on or off
            if GPIO.input(self.heat_pin) == '0 / GPIO.LOW / False':
                heater_status = 'off'
            elif GPIO.input(self.heat_pin) == '1 / GPIO.HIGH / True':
                heater_status = 'off'
            if GPIO.input(self.ac_pin) == '0 / GPIO.LOW / False':
                ac_status = 'off'
            elif GPIO.input(self.ac_pin) == '1 / GPIO.HIGH / True':
                ac_status = 'off'
            if GPIO.input(self.hum_pin) == '0 / GPIO.LOW / False':
                hum_status = 'off'
            elif GPIO.input(self.hum_pin) == '1 / GPIO.HIGH / True':
                hum_status = 'on'
            if self.current_temp <= self.thresholds['LL']:
                alert_type = 'Low-temp'
            elif self.current_temp >= self.thresholds['HH']:
                alert_type = 'High-temp'
            run_alert(
                      self.thresholds['HH'], 
                      self.thresholds['LL'], 
                      self.thresholds['HHUM'], 
                      self.thresholds['LHUM'], 
                      heater_status, 
                      ac_status, 
                      hum_status, 
                      alert_type
                      )

    def record(self):
        self.data_manager.update_data(self.current_temp, self.current_hum)
        self.data_manager.record_data()
        

    def run(self):
        while True:
            self.update_readings_from_sensor()
            self.record()


controller = ControlModule()

controller.run()