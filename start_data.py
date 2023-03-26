import time
from data_rec_init import TemperatureAndPressure
from data_rec_final import TemperatureAndPressureProcessor


class SensorRecorder:
    def __init__(self):
        self.tap = TemperatureAndPressure()
        self.tap_processor = TemperatureAndPressureProcessor()
        self.second_interval = 5
        self.minute_interval = 300

    def record_data(self):
        while True:
            current_time = round(time.time())
            if current_time % self.second_interval == 0:
                self.tap.record_data_to_csv()

            if current_time % self.minute_interval == 0:
                self.tap_processor.process_data()
            
            time.sleep(1)

recorder = SensorRecorder()

recorder.record_data()