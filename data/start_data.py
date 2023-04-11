import time
from write_raw import TemperatureAndHumidity
from write_final import TemperatureAndHumidityProcessor


class SensorRecorder:
    '''What runs and constantly records the data from the sensor'''

    def __init__(self):
        self.tap = TemperatureAndHumidity() #aka raw
        self.second_interval = 5 #Takes raw data every 5 seconds
        if not self.tap.test_mode:
            self.tap_processor = TemperatureAndHumidityProcessor() #aka dot
            self.minute_interval = 300 #Processes raw data every 5 minutes
            self.day_interval = 86,400 #Seconds in Day
        else:
            #IF TEST MODE ACTIVE, tap_processor = False, meaning no data gets saved in the main file and everything gets put in data/csv/test.csv
            self.tap_processor = False
            print("Start_data.py is in test mode")

    def record_data(self):

        while True:
            current_time = round(time.time())

            #Check for test mode and if the day has passed, if so start a new dot csv
            if self.tap_processor and current_time % self.minute_interval == 0:
                self.tap_processor.csv_name_is_current_date()

            #Checks for test mode and if 5 minutes have passed. If so, records data to dot
            if self.tap_processor and current_time % self.minute_interval == 0:
                self.tap_processor.process_data()

            #Checks to see if 5 seconds has passed, if so updates the raw. Works in Test mode or active mode.
            if current_time % self.second_interval == 0:
                self.tap.record_data_to_csv()




            
            time.sleep(1) #necessary so it doesn't run over and over in the same second

recorder = SensorRecorder()

recorder.record_data()