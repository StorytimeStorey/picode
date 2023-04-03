# Jeffrey the discord bot, Bonnibel but better
import discord
import info_parcer_2 as info
import asyncio
import multiprocessing as mp
# from alerts import pi_alerts
from discord.ext import tasks, commands
from discord import app_commands
from datetime import datetime

with open('../McJohnsonToken.txt') as f: token = f.read().strip()
guild_id = 705960639687950387
# initialize discord client
intents = discord.Intents.default
McJohnson = discord.Client(intents=intents)
channel = McJohnson.get_channel(guild_id)
# set command prefix
McJohnson = commands.Bot(command_prefix='@M')

@McJohnson.command(name='set_channel')
async def set_channel(ctx):
    McJohnson.default_channel = ctx.channel
    await ctx.send('Channel set.')

@McJohnson.hybrid_command
async def print_graphs():
    current_day = datetime.today().strftime('%d_%m_%y')
    csv_file = f'data/csv/{current_day}_dot.csv'
    save_location = "data/csv/"
    info.make_graph(csv_file, save_location)
    with open('data/csv/temperature_and_humidity.png', 'rb') as file:
        image = discord.File(file)
    await channel.send(file=image)

@McJohnson.hybrid_command
async def print_status():
    try:
        current_day = datetime.today().strftime('%d_%m_%y')
        current_status = info.read_last_row(f'data/csv/{current_day}_dot.csv')
        channel.send(f"{current_status}")
    except FileNotFoundError:
        channel.send("5-minute file doesn't exist yet. Pulling data from raw...")
        current_status = info.read_last_row('data/csv/raw.csv')
        channel.send(f"{current_status}")

def run_bot():
    McJohnson.run(token)

run_bot()