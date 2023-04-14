# Jeffrey the discord bot, Bonnibel but better
import discord
import info_parcer_2 as info
import asyncio
import multiprocessing as mp
# from alerts import pi_alerts
from discord.ext import tasks, commands
from discord import app_commands
from datetime import datetime
import os
import pandas as pd
# from new_alerts import write_alert
# import tracemalloc
# tracemalloc.start()

Storey_johnson_path = r'C:/Users/tomic/Desktop/johnson.txt'
Jackson_johnson_path = r'/Users/jackson/Documents/GitHub/picode/bot_2/McJohnsonToken.txt'
pi_johnson_path = r'../McJohnsonToken.txt'

guild_id = 705960639687950387 #Channel ID
channel_id = 1092481064087330957

# initialize discord client
intents = discord.Intents(value=7, 
                          guild_messages=True, 
                          guild_typing=True, 
                          message_content=True, 
                          messages=True, 
                          typing=True,
                          integrations=True)

Client = discord.Client(intents=intents)

# channel = Client.get_channel(channel_id)

# set command prefix
McJohnson = commands.Bot(command_prefix='@M', intents=intents)

#Not sure what this command is doing. Jackson, any comments here?
@McJohnson.command(name='set_channel')
async def set_channel(ctx):
    McJohnson.default_channel = ctx.channel
    await ctx.send('Channel set.')

@McJohnson.hybrid_command()
async def hello(ctx):
    await ctx.send("hello!")

@McJohnson.hybrid_command()
async def print_graphs(ctx): #This needs to be connected to a pipe in order to work properly, since it takes too long to work normally.
    if os.path.exists(pi_johnson_path):
        current_day = datetime.today().strftime('%d_%m_%y')
        csv_file = f'../data/{current_day}_dot.csv'
        save_location = "../data/" 
        info.make_graph(csv_file, save_location)
        with open('../data/temperature_and_humidity.png', 'rb') as file:
            image = discord.File(file)
        await ctx.send(file=image)


    else: #CODE FOR TESTING ENVIRONMENT
        csv_file = 'controller/data/csv/raw.csv'
        print(csv_file)
        save_location = 'controller/data/csv/'
        info.make_graph(csv_file, save_location)
        with open('controller/data/csv/test_temperature_and_humidity.png', 'rb') as file:
            image = discord.File(file)      
        await ctx.send(file=image)
#Not sure what this is...
    # await ctx.send(file=image).defer()
    # asyncio.sleep()
    # await ctx.followup.send()

@McJohnson.hybrid_command()
async def print_status(ctx):
    if os.path.exists(pi_johnson_path):
        try:
            current_day = datetime.today().strftime('%d_%m_%y')
            current_status = info.read_last_row(f'../data/{current_day}_dot.csv')
            await ctx.send(f"{current_status}")
        except FileNotFoundError:
            ctx.send("5-minute file doesn't exist yet. Pulling data from raw...")
            current_status = info.read_last_row('controller/data/csv/raw.csv')
            await ctx.send(f"{current_status}")



    else: #CODE FOR TESTING ENVIRONMENT
        current_status = info.read_last_row('controller/data/csv/test.csv')
        await ctx.send(f"{current_status}")
@McJohnson.hybrid_command()
# @commands.is_owner()
async def shutdown(ctx):
    exit()
    quit()

# @McJohnson.event
# async def send_alert(channel, alert_csv):
#     last_row = alert_csv.iloc[-1]
#     date = last_row[0]
#     time = last_row[1]
#     temp = last_row[2]
#     humidity = last_row[3]
#     alert_type = last_row[4]
#     heater_status = last_row[5]
#     ac_status = last_row[6]
#     humidifier_status = last_row[7]
#     await channel.send(f'On {date} at {time}, the following alert was found:\nAlert Type: {alert_type}\nTemperature: {temp}\nHumidity: {humidity}\nHeater Status: {heater_status}\nAC Status: {ac_status}\nHumidifier Status: {humidifier_status}')
# # loop to check if it needs to send an alert or not
# @tasks.loop(seconds=5)
# async def alert(channel):
#     # if len_alerts exists, check if the length has changed and send alert if it has. if it does not exist, create it
#     alert_csv = pd.read_csv('controller/data/csv/alerts.csv')
#     if not 'len_alerts' in globals():
#         global len_alerts
#         len_alerts = len(alert_csv)
#         print(len_alerts)
#     else:
#         if len(alert_csv) > len_alerts:
#             await send_alert(channel, alert_csv)
#             print('sent alert')
    # write_alert()

    # current_status = info.read_last_row('data/csv/test.csv')
    # await channel.send(f'{current_status}')

# syncs the task tree and start the alerts loop
@McJohnson.event
async def on_ready():
    await McJohnson.tree.sync()
    channel = McJohnson.get_channel(channel_id)
    # alert.start(channel)
    # exit()

def run_bot():
    if os.path.exists(Storey_johnson_path): #If Storey is testing...
        print("Storey path works")
        with open(Storey_johnson_path) as f: token = f.read().strip()
    elif os.path.exists(Jackson_johnson_path): #If Jackson is testing...
        print("Jackson_path works")
        with open(Jackson_johnson_path) as f: token = f.read().strip()
    elif os.path.exists(pi_johnson_path): #If run on the pi...
        print("pi_path works")
        with open(pi_johnson_path) as f: token = f.read().strip()
    else:
        print("Failed to find token") #Catches for failures...

    McJohnson.run(token)

run_bot()
