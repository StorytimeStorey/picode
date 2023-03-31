from current_sensor import Sensor
import os

class TemperatureAndPressure:
    def __init__(self):
        self.sensor = Sensor()
        self.csv = 'data/csv/raw.csv'

    def record_data_to_csv(self):
        self.sensor.update_readings()
        
        # Check if CSV file exists and create it with header row if it doesn't
        if not os.path.exists(self.csv):
            with open(self.csv, 'w') as f:
                f.write('Temperature (C),Pressure (hPa)\n')

        with open(self.csv, 'a') as f:
            f.write(f'{self.sensor.temperature},{self.sensor.pressure}\n')