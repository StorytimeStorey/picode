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

    def record_data(self):
        while True:
            current_time = round(time.time())
            if current_time % self.second_interval == 0:
                self.tap.record_data_to_csv()

            if current_time % self.minute_interval == 0:
                self.tap_processor.process_data()
            
            time.sleep(1) #necessary so it doesn't run over and over in the same second

recorder = SensorRecorder()

recorder.record_data()