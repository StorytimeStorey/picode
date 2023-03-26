import csv
import time
import os


class pi_alerts:
    def __init__(self, 
                 data_file = 'data/csv/raw.csv', 
                 alerts_file = 'data/csv/alerts.csv',
                 temp_vals_low = [50, 58],
                 temp_vals_high = [68, 72],
                 hum_vals_low = [85, 79]
                 ):
        self.data_file = data_file
        self.alerts_file = alerts_file
        self.minor_alarms = 0
        self.major_alarms = 0
        self.temp_vals_low = temp_vals_low #lowlow, low
        self.temp_vals_high = temp_vals_high #high, highhigh
        self.hum_vals_low = hum_vals_low #lowlow, low

        self.max_flags = 5
        self.total_temp_alerts_this_run = {}
        self.total_hum_alerts_this_run = {}

        self.reported_alerts = {}

    def check_temp(self, row):

        #test for low
        if row <= self.temp_vals_low[1]: 
            self.total_temp_alerts_this_run['temp_low'] += 1

        #test for lowlow
        if row <= self.temp_vals_low[0]:
            self.total_temp_alerts_this_run['temp_lowlow'] += 1

        #test for high
        if row >= self.temp_vals_low[0]:
            self.total_temp_alerts_this_run['temp_high'] += 1

        #test for highhigh
        if row >= self.temp_vals_low[1]:
            self.total_temp_alerts_this_run['temp_highhigh'] += 1

    def check_hum(self, row):

        #test for low
        if row <= self.temp_vals_low[1]: 
            self.total_hum_alerts_this_run['hum_low'] += 1

        #test for lowlow
        if row <= self.temp_vals_low[0]:
            self.total_hum_alerts_this_run['hum_lowlow'] += 1

    def check_values(self):
        
        self.total_temp_alerts_this_run = {} #reset counters
        if os.path.isfile(self.data_file):
            with open(self.data_file, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                
                for row in reader:
                    self.check_temp(row[0])
                    self.check_hum(row[1])
                
                for key,value in self.total_temp_alerts_this_run.items():
                    if value > self.max_flags:
                        self.reported_alerts[key] = time.strftime('%Y-%m-%d %H:%M:%S'), value
                        with open(self.alerts_file, 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), self.reported_alerts[key], value])
                        self.major_alarms += 1

                for key,value in self.total_hum_alerts_this_run.items():
                    if value > self.max_flags:
                        self.reported_alerts[key] = time.strftime('%Y-%m-%d %H:%M:%S'), value
                        with open(self.alerts_file, 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), self.reported_alerts[key], value])
                        self.major_alarms += 1