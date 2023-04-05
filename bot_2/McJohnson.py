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

Storey_johnson_path = r'C:/Users/tomic/Desktop/johnson.txt'
Jackson_johnson_path = r'/Users/jackson/Documents/GitHub/picode/bot_2/McJohnsonToken.txt'
pi_johnson_path = r'../McJohnsonToken.txt'

guild_id = 705960639687950387 #Channel ID

# initialize discord client
intents = discord.Intents(value=7, 
                          guild_messages=True, 
                          guild_typing=True, 
                          message_content=True, 
                          messages=True, 
                          typing=True,
                          integrations=True)

McJohnson = discord.Client(intents=intents)

channel = McJohnson.get_channel(guild_id)
# set command prefix
McJohnson = commands.Bot(command_prefix='@M', intents=intents)

#Not sure what this command is doing. Jackson, any comments here?
@McJohnson.command(name='set_channel')
async def set_channel(ctx):
    McJohnson.default_channel = ctx.channel
    await ctx.send('Channel set.')

@McJohnson.event
async def on_ready():
    await McJohnson.tree.sync()

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
        csv_file = 'data/csv/test.csv'
        print(csv_file)
        save_location = 'data/csv/'
        info.make_graph(csv_file, save_location)
        with open('data/csv/test_temperature_and_humidity.png', 'rb') as file:
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
            channel.send("5-minute file doesn't exist yet. Pulling data from raw...")
            current_status = info.read_last_row('data/csv/raw.csv')
            await ctx.send(f"{current_status}")



    else: #CODE FOR TESTING ENVIRONMENT
        current_status = info.read_last_row('data/csv/test.csv')
        await ctx.send(f"{current_status}")


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
