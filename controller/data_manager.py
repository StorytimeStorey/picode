import csv
import time
from datetime import datetime
import os



#class for writing to raw

class Data_Raw:
    '''Takes the current values from the sensor and writes them to a csv'''
    def __init__(self, csv = 'controller/data/csv/raw.csv'):
        self.csv = csv
        print("Raw Writer Initialized")

    def record_data_to_csv(self, temp, hum):
        # Check if CSV file exists and create it with header row if it doesn't
        if not os.path.exists(self.csv):
            with open(self.csv, 'w') as f:
                    f.write('Temperature,Humidity\n')

        with open(self.csv, 'a') as f:
            f.write(f'{temp},{hum}\n')


#class for processed data
class Data_Final:
    '''
    This takes in Temp and humidity from a raw csv (from Data_Raw class)
    Averages the data on that file and saves it to a dot.csv (data over time)
    See readme for implementation plans

    Another known error is that it sometimes saves at the _9/_4 mark instead of _0/_5 marks. Might be because I'm using time.time()
    
    '''
    def __init__(self):
        self.data_file = 'controller/data/csv/raw.csv'  #raw data
        current_day = datetime.today().strftime('%m_%d_%y')
        self.output_file = f'../data/{current_day}_dot.csv' #data over time
        self.data = []
        

    def csv_name_is_current_date(self):
        # Get the current date
        today = datetime.today()
        # Format the date as dd_mm_yyhumidity
        date_str = today.strftime('%m_%d_%y')
        #Update self.output_file name
        self.output_file = f'../data/{date_str}_dot.csv'


    def read_data_from_csv(self):
        self.data = [] #reset the list
        with open(self.data_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            self.data = [(float(row[0]), float(row[1])) for row in reader]
            
    def average_data(self):
        #function to average each column of data from the csv
        total_temperature = 0
        total_humidity = 0
        for temperature, humidity in self.data:
            total_temperature += temperature
            total_humidity += humidity
        avg_temperature = round(total_temperature / len(self.data), 1)  #Rounds it to one dec point
        avg_humidity = round(total_humidity / len(self.data),1)
        return avg_temperature, avg_humidity
        
    def write_averages_to_csv(self, avg_temperature, avg_humidity):
        #Writes to the csv
        time_now = datetime.now().strftime('%H%M')
        if not os.path.isfile(self.output_file): #Checks if file exists. If not, makes it with a header.
            with open(self.output_file, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['Time', 'Temp', 'Humidity'])
        with open(self.output_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([time_now, avg_temperature, avg_humidity])
            
    def clear_data_file(self):
        #This clears the raw file. raw should only keep about 5 minutes worth of data. No point in clogging everything up.
        #It's interesting that it works because it absolutely looks like it shouldn't lmao
        with open(self.data_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Temperature (C)', 'Humidity'])

    def process_data(self):
        #The function where everything happens
        self.read_data_from_csv()
        avg_temperature, avg_humidity = self.average_data()
        self.write_averages_to_csv(avg_temperature, avg_humidity)
        self.clear_data_file()


#class to manage the above two and their times of activation
class DataManager:
    '''Gets passed the current sensor readings and controls when data will be written to csv'''

    def __init__(self):
        self.raw_writer = Data_Raw() #aka raw
        self.data_processor = Data_Final() #aka dot
        self.second_interval = 5 #Takes raw data every 5 seconds
        self.minute_interval = 300 #Processes raw data every 5 minutes
        self.day_interval = 86400 #Seconds in Day
        self.temp = 0
        self.hum = 0
    
    def update_data(self, temp, hum):
        self.temp = temp
        self.hum = hum

    def record_data(self):
        current_time = round(time.time())
        #Check if the day has passed, if so start a new dot csv
        if current_time % self.day_interval == 0:
            self.data_processor.csv_name_is_current_date()

        #Checks if 5 minutes have passed. If so, records data to dot
        if current_time % self.minute_interval == 0:
            self.data_processor.process_data()

        #Checks to see if 5 seconds has passed, if so updates the raw. Works in Test mode or active mode.
        if current_time % self.second_interval == 0:
            self.raw_writer.record_data_to_csv(self.temp, self.hum)




        
        time.sleep(1) #necessary so it doesn't run over and over in the same second