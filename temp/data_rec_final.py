import csv
import time
from datetime import datetime


class TemperatureAndPressureProcessor:
    def __init__(self):
        self.data_file = 'Data/CSV/raw.csv'  #raw data
        self.output_file = 'Data/CSV/dot.csv' #data over time
        self.data = []
        
    def read_data_from_csv(self):
        with open(self.data_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            self.data = [(float(row[0]), float(row[1])) for row in reader]
            
    def average_data(self):
        total_temperature = 0
        total_pressure = 0
        for temperature, pressure in self.data:
            total_temperature += temperature
            total_pressure += pressure
        avg_temperature = round(total_temperature / len(self.data), 1)
        avg_pressure = round(total_pressure / len(self.data),1)
        return avg_temperature, avg_pressure
        
    def write_averages_to_csv(self, avg_temperature, avg_pressure):
        time_now = datetime.now().strftime('%H%M')
        with open(self.output_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([time_now, avg_temperature, avg_pressure])
            
    def clear_data_file(self):
        with open(self.data_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Temperature (C)', 'Pressure (hPa)'])

    def process_data(self):
        self.read_data_from_csv()
        avg_temperature, avg_pressure = self.average_data()
        self.write_averages_to_csv(avg_temperature, avg_pressure)
        self.clear_data_file()


if __name__ == '__main__':
    processor = TemperatureAndPressureProcessor()
    while True:
        processor.process_data()
        time.sleep(300)  # Wait 5 minutes
