
from current_sensor import Sensor
import os
from datetime import datetime


class TemperatureAndPressure:
    def __init__(self):
        self.sensor = Sensor()
        if not self.sensor.test_mode:     
            self.csv = 'data/csv/raw.csv'

        else: #CODE FOR TESTING ENVIRONMENT
            self.test_mode = True
            print("data_rec_init is in test mode")
            self.csv = 'data/csv/test.csv'

    def record_data_to_csv(self):
        self.sensor.update_readings()
        
        # Check if CSV file exists and create it with header row if it doesn't
        if not os.path.exists(self.csv):
            if not self.test_mode:
                with open(self.csv, 'w') as f:
                    f.write('Temperature,Pressure (hPa)\n')

            else: #CODE FOR TESTING ENVIRONMENT
                with open(self.csv, 'w') as f:
                    f.write('Time,Temp,Humidity\n')         

        if not self.test_mode:
            with open(self.csv, 'a') as f:
                f.write(f'{self.sensor.temperature},{self.sensor.pressure}\n')

        else: #CODE FOR TESTING ENVIRONMENT
            time_now = datetime.now().strftime('%H%M%S')
            with open(self.csv, 'a') as f:
                f.write(f'{time_now},{self.sensor.temperature},{self.sensor.pressure}\n')