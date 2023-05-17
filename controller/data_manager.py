import csv
import time
from datetime import datetime
import os
import math
import sqlite3


#class for writing to raw

class Data_Raw:
    ''' Takes the current values from the sensor and writes them to a csv '''
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
    '''
    SQLite database management for data quering and storage
    database filename assumed in this case to be "box1.db"
    Further development will probably require a better naming convention and variable control for that.
    Currently the program can only handle one sensor input, so this will probably remain the case for a while.
    '''
    def __init__(self, filename):
        self.filename = filename
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        ''' SQLite coding is confusing. Unsure if with this code that the column's name are now stuck as "value1" and "value2" '''
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
    This class manages the final step for inserting recorded data into a SQLite database
    It has the functions:
        1) Read data from csv
        2) average data
        3) write averages to database
        4) clear data file
        5) process data
    1-4 are functions operated by function 5. You will probably only see the process data function outside of this class.
    This class initializes with the following directory for the location of the raw csv file:
        'controller/data/csv/raw.csv'
    And saves to a database stored in a folder currently outside of the main code folder:
        "../data/box1.db"
    '''
    def __init__(self):
        self.data_file = 'controller/data/csv/raw.csv'  #raw csv
        self.data = []

        self.db = Database("../data/box1.db")

    def read_data_from_csv(self):
        ''' sets self.data to the current set of data from RAW '''
        self.data = [] #reset the list
        with open(self.data_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            self.data = [(float(row[0]), float(row[1])) for row in reader]
            
    def average_data(self):
        ''' function to average temp and humidity data from the csv '''
        total_temperature = 0
        total_humidity = 0
        for temperature, humidity in self.data:
            total_temperature += temperature
            total_humidity += humidity
        avg_temperature = round(total_temperature / len(self.data), 1)  #Rounds it to one dec point
        avg_humidity = round(total_humidity / len(self.data),1)
        return avg_temperature, avg_humidity
    
    def write_averages_to_db(self, avg_temp, avg_hum):
        '''Makes a timestamp in the form Y-m-d H:M:S and averaged temps and humidities from RAW and inserts it into the database'''
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.db.insert_data(timestamp, avg_temp, avg_hum)
        

    def clear_data_file(self):
        ''' This clears the raw file. raw should only keep about 5 minutes worth of data. No point in clogging everything up.
            It's interesting that it works because it absolutely looks like it shouldn't lmao'''
        with open(self.data_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Temperature (C)', 'Humidity'])

    def process_data(self):
        '''Reads the raw CSV, averages the numbers, writes the average to the database, and clears the raw CSV'''
        #The function where everything happens
        self.read_data_from_csv()
        avg_temperature, avg_humidity = self.average_data()
        self.write_averages_to_db(avg_temperature,avg_humidity)
        # self.write_averages_to_csv(avg_temperature, avg_humidity)
        self.clear_data_file()


#class to manage the above two and their times of activation
class DataManager:
    '''
        This class gets all the others in data_manager.py passed to it. Everything should be happening here.
        Data_Raw class initializes at self.raw_writer and takes sensor data and records it into a raw.csv
            This happens every 5 seconds
        Data_Final class initializes at self.data_processor. It averages the data from raw.csv and saves it to the SQLite database
            This happens every 5 minutes
        This class utilizes the time.sleep function in its main run function (called record_data). 
        This means that occasionally there are missed events. The frequency and its effects are, as far as we can tell, negligable. 
    '''

    def __init__(self):
        self.raw_writer = Data_Raw() #aka raw
        self.data_processor = Data_Final() #aka dot
        self.second_interval = 5 #Takes raw data every 5 seconds
        self.minute_interval = 300 #Processes raw data every 5 minutes
        self.temp = 0
        self.hum = 0
    
    def update_data(self, temp, hum):
        '''
            Must be run from where the sensor is being called. Probably the Controller.
            This function literally only looks like:
            self.temp = temp
            self. hum = hum
            with temp, hum being passed from a get_readings function from the Controller function.

            The reason this happens is recording is a secondary priority. The first priority for this entire program is to ensure
            that the temperature and humidity are within a range, and if not activate controlling elements (heater, cooler, humidifier) AND 
            if values climb far out of normalcy to alert the user via the bot. 
            Therefore the sensor is updated elsewhere, the values are checked for alarms, THEN they are written to raw and saved to the database. 
        '''
        self.temp = temp
        self.hum = hum

    def record_data(self):
        '''
            Where everything in Data_Manager happens.
            Take current time and round it (down)
            if the current time % either the minute or the second interval chosen, it'll activate either recording data to csv or 
        '''
        current_time = math.floor(time.time())
        #Checks if 5 minutes have passed. If so, records data to dot
        if current_time % self.minute_interval == 0:
            self.data_processor.process_data()

        #Checks to see if 5 seconds has passed, if so updates the raw. Works in Test mode or active mode.
        if current_time % self.second_interval == 0:
            self.raw_writer.record_data_to_csv(self.temp, self.hum)
        
        time.sleep(1) #necessary so it doesn't run over and over in the same second