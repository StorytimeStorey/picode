import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sqlite3



def trim_data_list(data):
    '''
    Takes in a list, returns a trimmed list based on the total length of the list.

    Discord only allows 2000 characters per post. This function makes sure that a list of values
    is less than that amount. It is calculated using 35 characters per line. This allows for 47 lines from the list.
    This function will eventually have use a second variable to control the divisor for different uses. 
    '''
    if len(data) > 47:
        step = len(data) // 47
        trimmed_data = data[::step]
        return trimmed_data
    else:
        return data



def get_data_from_db(datatype_queried, timeline_queried):
    '''Takes in a datatype "humidity" or "temperature" and a timeline "10 minutes" or "5 days" and gets the data from the 
    database
    data is a list: [place in list, timestamp, temperature, humidity]
    final data list comes in 3 forms:
        timestamp, temp
        timestamp, hum
        timestamp, temp, hum
    '''
    #connect to the db
    conn = sqlite3.connect("../data/box1.db")
    c = conn.cursor()
    start_time = parse_duration(timeline_queried)
    #Find the amount of time between now and requested time
    timeline = datetime.now() - start_time

    c.execute("SELECT * FROM data WHERE timestamp >= ?", (timeline,))
    data = trim_data_list(c.fetchall())

    datatype = parse_datatype(datatype_queried)
    if datatype == "temp":
        requested_data = [(row[1], row[2]) for row in data]
    elif datatype == "hum":
        requested_data = [(row[1], row[3]) for row in data]
    elif datatype == "both":
        requested_data = [(row[1], row[2], row[3]) for row in data]

    conn.close()
    return requested_data, datatype

def parse_datatype(datatype_str):
    '''Checks to see which datatype is being requested
        Temperature, Humidity, and Both or All.
        simply checks if the first letter is t, h, b, or a'''
    if datatype_str[0].lower() == "h":
        return "hum"
    elif datatype_str[0].lower() == "t":
        return "temp"
    elif datatype_str[0].lower() == "b" or datatype_str[0].lower() == "a":
        return "both"
    else: 
        raise ValueError(f"Invalid datatype {datatype_str}")


def parse_duration(duration_str):
    '''
    Takes the duration string from discord input and parces out the pieces
    Checks for a number in the beginning and a word at the end
    Turns the number into some form of seconds 
    '''
    duration = 0
    val, txt = duration_str.split()
    try:
        value = int(val)
    except ValueError:
        raise ValueError(f"Invalid duration value: {val}")
    txt.lower()
    if "second" in txt:
        duration += value
    elif "min" in txt:
        duration += value * 60
    elif "hour" in txt:
        duration += value * 3600
    elif "day" in txt:
        duration += value * 86400
    elif "week" in txt:
        duration += value * 604800
    else:
        raise ValueError("Invalid duration unit: {}".format(txt))
    return timedelta(seconds = duration)

def generate_text_from_csv_list(list):
    if len(list) > 2:

        last_time = list[0]
        last_temp = list[1]
        last_humidity = list[2]
        # heater_on = "On" if list[3] == 1 else "off"
        # cooler_on = "On" if list[4] == 1 else "off"
        # humidifier_on = "On" if list[5] == 1 else "off"
        # alerts = "YES" if list[6] == 1 else "NO"
        # status_text = f"Last data taken at {last_time}.\nTemperate: {last_temp}.\nHumidity: {last_humidity}\nHeater: {heater_on}\nCooler: {cooler_on}\nHumidifier: {humidifier_on}\nAlerts: {alerts}"
        status_text = f"Last data taken at {last_time}.\nTemperature: {last_temp}.\nHumidity: {last_humidity}"
    else:
        time_now = datetime.now().strftime('%H%M')
        status_text = f"Last data taken at {time_now}.\nTemperature: {list[0]}.\nHumidity: {list[1]}"
    return status_text

def read_last_row(file_path):
    # Open the CSV file
    with open(file_path, 'r') as csvfile:
        # Create a CSV reader
        reader = csv.reader(csvfile)

        # Read all the rows into a list
        rows = list(reader)

        # Get the last row
        data_list = rows[-1]
    
    text = generate_text_from_csv_list(data_list)
        # Return the list
    return text

def create_graph(datatype_queried, timeline_queried):
    data, datatype = get_data_from_db(datatype_queried, timeline_queried)

    timestamp = [row[0] for row in data]
    if datatype == "temp":
        temp = [row[1] for row in data]
        plt.plot(timestamp, temp)
    elif datatype == "hum":
        hum = [row[1] for row in data]
        plt.plot(timestamp, hum)
    elif datatype == "both":
        temp = [row[1] for row in data]
        hum = [row[2] for row in data]
        plt.plot(timestamp, temp, label='Temperature')
        plt.plot(timestamp, hum, label='Humidity')

    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Data Graph')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{"../data"}/temperature_and_humidity.png', dpi=300)
    plt.close()
    



def make_graph(csv_file, data_directory):

    def xtick_counter(times:list):
        x_points_count = 12
        if len(times) < x_points_count:
            return len(times)
        else:
            return int(len(times)/x_points_count)
        
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # Extract the temperature and humidity data
    times = [row['Time'] for row in data]
    temperatures = [float(row['Temp']) for row in data]
    x_points_count = 12
    #humidities = [float(row['Humidity']) for row in data]

    # Create the plot
    plt.plot(times, temperatures, label='Temperature')
   # plt.plot(times, humidities, label='Humidity')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Temperature and Humidity Over Time')
    plt.legend()
    plt.xticks(range(0, len(times), int(len(times)/x_points_count)), times[::int(len(times)/x_points_count)], fontsize=8)
    plt.xlim(times[0], times[-1])

    if csv_file == 'controller/data/csv/test.csv':
        plt.savefig(f'{data_directory}/test_temperature_and_humidity.png', dpi=300)
    else:
        plt.savefig(f'{data_directory}/temperature_and_humidity.png', dpi=300)
    
    plt.close()



def add_time_column(data):
    time = 1
    new_data = [['Time', 'Temp', 'Humidity']]
    for row in data[1:]:
        new_row = [time] + row
        new_data.append(new_row)
        time += 1
    return new_data


if __name__ == '__main__':

    data = read_last_row('Temp_Example.csv')
    print(data)