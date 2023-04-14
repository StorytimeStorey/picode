import pandas as pd
import time

class Alert:
    '''
    Creates alerts and writes them to a csv file
    Should be called from another function which detects if an alert needs to be made
    '''
    def __init__(
                self, 
                upper_temp, 
                lower_temp, 
                upper_humidity, 
                lower_humidity,
                heater_status,
                ac_status,
                hum_status,
                alert_type
                ):
        self.upper_temp = upper_temp
        self.lower_temp = lower_temp
        self.upper_humidity = upper_humidity
        self.lower_humidity = lower_humidity
        self.heater_status = heater_status
        self.ac_status = ac_status
        self.hum_status = hum_status
        self.alert_type = alert_type
        # creates variables for all time types needed
        self.time_struct = time.localtime()
        self.current_date = f'{self.time_struct[1]}-{self.time_struct[2]}-{self.time_struct[0]}'
        self.current_time = f'{self.time_struct[3]}:{self.time_struct[4]}'
        self.test_mode = False 
        # determine whether or not we are in testing mode
        try:
            self.raw_csv = pd.read_csv('data/csv/raw.csv')
        except FileNotFoundError:
            self.raw_csv = pd.read_csv('data/csv/test.csv')
            self.test_mode = True

        self.alerts_csv = pd.read_csv('data/csv/alerts.csv')

    def get_status(self):

        if not self.test_mode:
            num_rows = len(self.raw_csv.index)
            last_row = self.raw_csv.iloc[num_rows-1]
            self.current_temp = last_row['Temp']
            self.current_humidity = last_row['Humidity']
        else: 
            num_rows = len(self.raw_csv.index)
            last_row = self.raw_csv.iloc[num_rows-1]
            self.current_temp = last_row['Temp']
            self.current_humidity = last_row['Humidity']

    def write_alert(self):
        # get current status of temp and humidity
        self.get_status()
        # appends the following(obviously name) values to the alerts csv
        self.alerts_csv.at[len(self.alerts_csv)+1,'Date'] = self.current_date
        self.alerts_csv.at[len(self.alerts_csv),'Time'] = self.current_time
        self.alerts_csv.at[len(self.alerts_csv),'Temp'] = self.current_temp
        self.alerts_csv.at[len(self.alerts_csv),'Humidity'] = self.current_humidity
        self.alerts_csv.at[len(self.alerts_csv),'Alert Type'] = self.alert_type
        self.alerts_csv.at[len(self.alerts_csv),'Heater Status'] = self.heater_status
        self.alerts_csv.at[len(self.alerts_csv),'AC Status'] = self.ac_status
        self.alerts_csv.at[len(self.alerts_csv),'Humidifier Status'] = self.hum_status
        # updates the csv file
        self.alerts_csv.to_csv('data/csv/alerts.csv', index=False)

def run_alert(upper_temp, lower_temp, upper_humidity, lower_humidity, heater_status, ac_status, hum_status, alert_type):
    alert = Alert(upper_temp, lower_temp, upper_humidity, lower_humidity, heater_status, ac_status, hum_status, alert_type)
    alert.write_alert()
