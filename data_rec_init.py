from current_sensor import Sensor

class TemperatureAndPressure:
    def __init__(self):
        self.sensor = Sensor()
        self.csv = 'temperature_and_pressure.csv'

    def record_data_to_csv(self):
        while True:
            self.sensor.update_readings()
            with open(self.csv, 'a') as f:
                f.write(f'{self.sensor.temperature},{self.sensor.pressure}\n')