test_mode = False

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Entering test mode")
    test_mode = True

from data_manager import DataManager
from sensor import BME280
from time import sleep
from new_alerts import run_alert

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
    3)writes to raw.csv to be processed by data-dir scripts
    
    '''
    def __init__(self, thresholds, heat_pin: int, ac_pin: int, hum_pin: int, fan_pin: int, light_pin: int):
        '''
        Initializes sensor, DataManager, and GPIO pins
        '''
        self.sensor = BME280() #Reach sensor
        self.data_manager = DataManager() #What controls writing and saving the data

        self.thresholds = thresholds
        # set the GPIO pins to use
        self.heat_pin = heat_pin
        self.ac_pin = ac_pin
        self.hum_pin = hum_pin
        self.fan_pin = fan_pin
        self.light_pin = light_pin
        # set the pins as output and turn them off
        GPIO.setup(self.heat_pin, GPIO.OUT)
        GPIO.setup(self.ac_pin, GPIO.OUT)
        GPIO.setup(self.hum_pin, GPIO.OUT)
        GPIO.setup(self.fan_pin, GPIO.OUT)
        GPIO.setup(self.light_pin, GPIO.OUT)
        GPIO.output(self.heat_pin, False)
        GPIO.output(self.ac_pin, False)
        GPIO.output(self.hum_pin, False)
        GPIO.output(self.fan_pin, False)
        GPIO.output(self.light_pin, False)

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
        # turn heater on if temp is too low
        if self.current_temp <= self.thresholds['HON']:
            GPIO.output(self.heat_pin, True)
            GPIO.output(self.ac_pin, False)
        # turn heater off if temp is good
        if self.current_temp >= self.thresholds['HOFF']:
            GPIO.output(self.heat_pin, False)
        # turn ac on if temp is too high
        if self.current_temp >= self.thresholds['CON']:
            GPIO.output(self.ac_pin, True)
            GPIO.output(self.heat_pin, False)
        # turn ac off if temp is good
        if self.current_temp <= self.thresholds['COFF']:
            GPIO.output(self.ac_pin, False)
        # turn humidifier on if humidity is too low
        if self.current_hum <= self.thresholds['HUMON']:
            GPIO.output(self.hum_pin, True)
        # turn humidifier off if humidity is good
        if self.current_hum >= self.thresholds['HUMOFF']:
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
        

    
