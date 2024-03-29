
import discord
import info_parcer as info
from discord.ext import tasks, commands
import os
import pandas as pd
import json


def read_line_from_file(line_number):
    '''Retrieves information from the help.txt
        line_number corresponds to the specific line requested. 0 will be the help line, 1 credits, etc.'''
    with open('bot/help.txt', 'r') as file:
        lines = file.readlines()
        line = lines[line_number]
        return line.strip().replace(r'\n', '\n')

def make_table(data, table_type):
    # Format data as a table
    if table_type == "temp" or table_type == "hum":
        table = "```\n"
        table += f"Date                |{table_type.capitalize()}\n"  # Table header
        table += "--------------------|\n"  # Table separator
        for row in data:
            table += f"{row[0]} | {row[1]}\n"
        table += "```"
        return table
    else:
        table = "```\n"
        table += f"Date                | Temp | Hum  |\n"  # Table header
        table += "--------------------|------|------|\n"  # Table separator
        for row in data:
            table += f"{row[0]} | {row[1]} | {row[2]} |\n"
        table += "```"
        return table


# finds the channel id and token paths from settings.json
with open("controller/settings.json", 'r') as file:
    data = json.load(file)
    channel_id = data["Channel_Id"]
    # set variables for the paths from json
    token_paths = data["Token_Paths"]
    pi_path = token_paths["pi_path"]
    # determine which path to use
    if os.path.exists(pi_path): 
        print("using pi_path")
        path = pi_path
        with open(path) as f: token = f.read().strip()
    else:
        for i in range(len(token_paths)-1):
            print(i)
            # check all the test paths and set it to the right one for the current running device
            if token_paths[f"test_path_{i}"] and os.path.exists(token_paths[f"test_path_{i}"]):
                path = token_paths[f"test_path_{i}"]
                print(path)
                with open(path) as f: token = f.read().strip()
                break

# initialize discord client
intents = discord.Intents(value=7, 
                          guild_messages=True, 
                          guild_typing=True, 
                          message_content=True, 
                          messages=True, 
                          typing=True,
                          integrations=True)

# set command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

#Not sure what this command is doing. Jackson, any comments here?
@bot.command(name='set_channel')
async def set_channel(ctx):
    bot.default_channel = ctx.channel
    await ctx.send('Channel set.')


@bot.hybrid_command()
async def graph(ctx,datatype, timeline, ):
    await ctx.defer()
    info.create_graph(datatype,timeline)
    with open('../data/temperature_and_humidity.png', 'rb') as file:
        image = discord.File(file)
    await ctx.send(file=image)

@bot.hybrid_command()
async def instructions(ctx):
    line = read_line_from_file(0)
    await ctx.send(line)

@bot.hybrid_command()
async def database(ctx, datatype, timeline):
    requested_data, parsed_datatype = info.get_data_from_db(datatype, timeline, 'print')
    table = make_table(requested_data, parsed_datatype)
    await ctx.send(table)


@tasks.loop(seconds=30)
async def change_status():
    try:
        current_status = info.read_last_row('controller/data/csv/raw.csv')
    except:
        current_status = "data not available, trying again..."
    await bot.change_presence(activity=discord.Game(f"{current_status}"))


@bot.command()
# @commands.is_owner()
async def shutdown(ctx):
    exit()
    quit()

@bot.event
async def send_alert(channel, alert_csv):
    last_row = alert_csv.iloc[-1]
    date = last_row[0]
    time = last_row[1]
    temp = last_row[2]
    humidity = last_row[3]
    alert_type = last_row[4]
    heater_status = last_row[5]
    ac_status = last_row[6]
    humidifier_status = last_row[7]
    await channel.send(f'On {date} at {time}, the following alert was found:\nAlert Type: {alert_type}\nTemperature: {temp}\nHumidity: {humidity}\nHeater Status: {heater_status}\nAC Status: {ac_status}\nHumidifier Status: {humidifier_status}')
# loop to check if it needs to send an alert or not

@tasks.loop(seconds=5)
async def alert(channel):
    alert_csv = pd.read_csv('controller/data/csv/alerts.csv')
    if 'len_alerts' not in globals():
        global len_alerts
        len_alerts = len(alert_csv)
    else:
        if len(alert_csv) > len_alerts:
            await send_alert(channel, alert_csv)
            print('sent alert')

    current_status = info.read_last_row('data/csv/test.csv')
    if current_status is not None:  # Add a check for None value
        await channel.send(f'{current_status}')

# syncs the task tree and start the alerts loop
@bot.event
async def on_ready():
    await bot.tree.sync()
    channel = bot.get_channel(channel_id)
    #alert.start(channel)
    change_status.start()
    # exit()

if __name__ == '__main__':
    bot.run(token)
