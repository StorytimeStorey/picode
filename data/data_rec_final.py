import csv
import time
from datetime import datetime
import os


class TemperatureAndPressureProcessor:
    '''
    Names are confusing, I'm sorry.
    This takes in Temp and Press (eventually humidity) from a raw csv (from data_rec init)
    Averages the data on that file and saves it to a dot.csv (data over time)
    See readme for implementation plans

    It just occurred to me self.data might never reset. Needs to be looked into...
    Another known error is that it sometimes saves at the _9/_4 mark instead of _0/_5 marks. Might be because I'm using time.time()
    
    '''
    def __init__(self):
        self.data_file = 'data/csv/raw.csv'  #raw data
        current_day = datetime.today().strftime('%d_%m_%y')
        self.output_file = f'data/csv/{current_day}_dot.csv' #data over time
        self.data = []
        

    def csv_name_is_current_date(self):
        # Get the current date
        today = datetime.today()
        # Format the date as dd_mm_yy
        date_str = today.strftime('%d_%m_%y')
        #Update self.output_file name
        self.output_file = f'data/csv/{date_str}_dot.csv'


    def read_data_from_csv(self):
        with open(self.data_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            self.data = [(float(row[0]), float(row[1])) for row in reader]
            
    def average_data(self):
        #function to average each column of data from the csv
        total_temperature = 0
        total_pressure = 0
        for temperature, pressure in self.data:
            total_temperature += temperature
            total_pressure += pressure
        avg_temperature = round(total_temperature / len(self.data), 1)  #Rounds it to one dec point
        avg_pressure = round(total_pressure / len(self.data),1)
        return avg_temperature, avg_pressure
        
    def write_averages_to_csv(self, avg_temperature, avg_pressure):
        #Writes to the csv
        time_now = datetime.now().strftime('%H%M')
        if not os.path.isfile(self.output_file): #Checks if file exists. If not, makes it with a header.
            with open(self.output_file, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['Time', 'Temp', 'Humidity'])
        with open(self.output_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([time_now, avg_temperature, avg_pressure])
            
    def clear_data_file(self):
        #This clears the raw file. raw should only keep about 5 minutes worth of data. No point in clogging everything up.
        #It's interesting that it works because it absolutely looks like it shouldn't lmao
        with open(self.data_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Temperature (C)', 'Pressure (hPa)'])

    def process_data(self):
        #The function where everything happens
        self.read_data_from_csv()
        avg_temperature, avg_pressure = self.average_data()
        self.write_averages_to_csv(avg_temperature, avg_pressure)
        self.clear_data_file()


if __name__ == '__main__':
    processor = TemperatureAndPressureProcessor()
    while True:
        processor.process_data()
        time.sleep(300)  # Wait 5 minutes
