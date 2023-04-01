import csv
import matplotlib.pyplot as plt
from datetime import datetime




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
        status_text = f"Last data taken at {last_time}.\nTemperate: {last_temp}.\nPressure: {last_humidity}"
    else:
        time_now = datetime.now().strftime('%H%M')
        status_text = f"Last data taken at {time_now}.\nTemperate: {list[0]}.\nPressure: {list[1]}"
    return status_text

def read_last_row(file_path):
    # Open the CSV file
    with open(file_path, 'r') as csvfile:
        # Create a CSV reader
        reader = csv.reader(csvfile)

        # Read all the rows into a list
        rows = list(reader)

        # Get the last row
        last_row = rows[-1]

        # Convert the last row data to a list
        data_list = [float(x) for x in last_row]
    
    text = generate_text_from_csv_list(data_list)
        # Return the list
    return text

def make_graph(csv_file, data_directory):

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # Extract the temperature and humidity data
    times = [row['Time'] for row in data]
    temperatures = [float(row['Temp']) for row in data]
    #humidities = [float(row['Humidity']) for row in data]

    # Create the plot
    plt.plot(times, temperatures, label='Temperature')
   # plt.plot(times, humidities, label='Humidity')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Temperature and Humidity Over Time')
    plt.legend()
    plt.savefig(f'{data_directory}/temperature_and_humidity.png', dpi=300)


if __name__ == '__main__':

    data = read_last_row('Temp_Example.csv')
    print(data)
