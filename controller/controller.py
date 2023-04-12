test_mode = False

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Entering test mode")
    test_mode = True

import start_data
import BME_280




class Control_Module:
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
    def __init__(self, heat_threshold, cold_threshold, humidity_threshold):

        self.sensor = BME_280.Sensor() #Reach sensor

        self.data_writing_module = start_data() #What controls writing and saving the data

        self.heat_threshold = heat_threshold #set thresholds for low (on) and high (off) for relays
        self.cold_threshold = cold_threshold
        self.humidity_threshold = humidity_threshold


        #Should be immediately changed by sensor updates
        self.current_temp = 0
        self.current_hum = 0

    def update_readings_from_sensor(self):
        self.sensor.update_readings()
        self.current_temp = self.sensor.temperature
        self.current_hum = self.sensor.humidity


    def check_vs_thresholds(self):
        #do stuff to check allowed thresholds 
        #turn off/on relays when needed
        #if beyond accepted thresholds, check vs alarm values
        pass

    def initialize_data(self):
        self.data_writing_module.record_data()
        pass
        
    def control_relay(self):
        temperature, humidity = self.read_sensor_data()
        if temperature >= self.temperature_threshold or humidity >= self.humidity_threshold:
            if not self.is_relay_on:
                GPIO.output(self.relay_pin, GPIO.HIGH)
                self.is_relay_on = True
        else:
            if self.is_relay_on:
                GPIO.output(self.relay_pin, GPIO.LOW)
                self.is_relay_on = False
