import csv
import time
import os


class pi_alerts:
    '''
    Checks values in a csv for temps or humidities higher or lower than the desired values
    Should eventually send alerts to Bonnibel to send them to discord
    see readme for more details regarding alert implementation plans

    Searches through a raw csv and if any values ping an alert, will increment a "max flags" variable. Once the number alerts surpases max allowed, it will trigger an alarm.

    uses lowlow, low, high, highhigh. This implimentation originates from alarm types seen at Hetchy. 
    
    
    '''
    def __init__(self, 
                 data_file = 'data/csv/raw.csv', #file it checks
                 alerts_file = '../data/alerts.csv', #file it will save alerts to with details. Currently not implemented
                 temp_vals_low = [50, 58], #lowlow, low
                 temp_vals_high = [68, 72], #high, highhigh
                 hum_vals_low = [85, 79] #low, lowlow
                 ):
        self.data_file = data_file
        self.alerts_file = alerts_file

        #major alarms and minor alarms unimplemented yet
        #intent is to 
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
        '''
        Exists inside the check_values function. Checks a row of values from csv against each chosen value.
        I've seen a super clean way to do this using dictionary composition but I wasn't sure how it worked. Might be worth looking into.
        self.total_temp_alerts and self.total_hum_alerts can probably be combined.
        '''
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
        '''
        All the actual checking happens here.
        Takes in the cvs file, iterates through each line and checks each value against target
        If # of alerts surpasses max_flags, writes the alert to a file, and increments major_alarms to 1
        '''
        self.total_temp_alerts_this_run = {} #reset counters

        #check to see if the file exists
        if os.path.isfile(self.data_file):
            with open(self.data_file, 'r') as f:
                reader = csv.reader(f)
                next(reader) #go past the header line
                
                for row in reader:
                    self.check_temp(row[0])
                    self.check_hum(row[1])
                

                #After going through each row, this checks for how many alerts it found.
                #If it found any, raises major_alarms and writes to a csv the time and kind of alarm.
                #Eventually I'd like to combine these 2 into one function. I don't like having this many lines out.
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