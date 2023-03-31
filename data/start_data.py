import time
from data_rec_init import TemperatureAndPressure
from data_rec_final import TemperatureAndPressureProcessor


class SensorRecorder:
    '''What runs and constantly records the data from the sensor'''
    def __init__(self):
        self.tap = TemperatureAndPressure() #aka raw
        self.tap_processor = TemperatureAndPressureProcessor() #aka dot
        self.second_interval = 5 #Takes raw data every 5 seconds
        self.minute_interval = 300 #Processes raw data every 5 minutes
        self.day_interval = 86,400 #Seconds in Day

    def record_data(self):
        while True:
            current_time = round(time.time())

            #Check for if the day has passed, if so start a new dot csv
            if current_time % self.minute_interval == 0:
                self.tap_processor.csv_name_is_current_date()

            #Checks to see if 5 minutes have passed. If so, records data to dot
            if current_time % self.minute_interval == 0:
                self.tap_processor.process_data()

            #Checks to see if 5 seconds has passed, if so updates the raw
            if current_time % self.second_interval == 0:
                self.tap.record_data_to_csv()




            
            time.sleep(1) #necessary so it doesn't run over and over in the same second

recorder = SensorRecorder()

recorder.record_data()