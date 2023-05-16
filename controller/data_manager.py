import csv
import time
from datetime import datetime
import os
import math
import sqlite3


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


class Database:
    '''SQLite database management for data quering and storage'''
    def __init__(self, filename):
        self.filename = filename
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                value1 REAL,
                value2 REAL
            )
        ''')
        self.connection.commit()

    def insert_data(self, timestamp, value1, value2):
        self.cursor.execute('''
            INSERT INTO data (timestamp, value1, value2)
            VALUES (?, ?, ?)
        ''', (timestamp, value1, value2))
        self.connection.commit()

    def get_data(self, since):
        self.cursor.execute('''
            SELECT * FROM data
            WHERE timestamp >= ?
        ''', (since,))
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()



#class for processed data
class Data_Final:
    '''
    This takes in Temp and humidity from a raw csv (from Data_Raw class)
    Averages the data on that file and saves it to a sqlite database
    See readme for implementation plans    
    '''
    def __init__(self):
        self.data_file = 'controller/data/csv/raw.csv'  #raw data
        self.data = []

        self.db = Database("../data/box1.db")

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
    
    def write_averages_to_db(self, avg_temp, avg_hum):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.db.insert_data(timestamp, avg_temp, avg_hum)
        

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
        self.write_averages_to_db(avg_temperature,avg_humidity)
        # self.write_averages_to_csv(avg_temperature, avg_humidity)
        self.clear_data_file()


#class to manage the above two and their times of activation
class DataManager:
    '''Gets passed the current sensor readings and controls when data will be written to csv'''

    def __init__(self):
        self.raw_writer = Data_Raw() #aka raw
        self.data_processor = Data_Final() #aka dot
        self.second_interval = 5 #Takes raw data every 5 seconds
        self.minute_interval = 300 #Processes raw data every 5 minutes
        self.temp = 0
        self.hum = 0
    
    def update_data(self, temp, hum):
        self.temp = temp
        self.hum = hum

    def record_data(self):
        current_time = math.floor(time.time())
        #Checks if 5 minutes have passed. If so, records data to dot
        if current_time % self.minute_interval == 0:
            self.data_processor.process_data()

        #Checks to see if 5 seconds has passed, if so updates the raw. Works in Test mode or active mode.
        if current_time % self.second_interval == 0:
            self.raw_writer.record_data_to_csv(self.temp, self.hum)
        
        time.sleep(1) #necessary so it doesn't run over and over in the same second