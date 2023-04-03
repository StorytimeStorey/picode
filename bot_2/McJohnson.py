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
intents = discord.Intents(value=7, 
                          guild_messages=True, 
                          guild_typing=True, 
                          message_content=True, 
                          messages=True, 
                          typing=True,
                          integrations=True)
McJohnson = discord.Client(intents=intents)
client = discord.Client(intents=intents)
channel = McJohnson.get_channel(guild_id)
# set command prefix
McJohnson = commands.Bot(command_prefix='@M', intents=intents)

@client.event
async def on_ready(ctx):
    McJohnson.default_channel = ctx.channel
    await ctx.send('Channel set.')
    await McJohnson.tree.sync()

@McJohnson.hybrid_command()
async def hello(ctx):
    await ctx.send("hello!")

@McJohnson.hybrid_command()
async def print_graphs(ctx):
    current_day = datetime.today().strftime('%d_%m_%y')
    csv_file = f'../data/{current_day}_dot.csv'
    save_location = "data/csv/"
    info.make_graph(csv_file, save_location)
    with open('../data/temperature_and_humidity.png', 'rb') as file:
        image = discord.File(file)
    await ctx.send(file=image)

@McJohnson.hybrid_command()
async def print_status(ctx):
    try:
        current_day = datetime.today().strftime('%d_%m_%y')
        current_status = info.read_last_row(f'../data/{current_day}_dot.csv')
        channel.send(f"{current_status}")
    except FileNotFoundError:
        channel.send("5-minute file doesn't exist yet. Pulling data from raw...")
        current_status = info.read_last_row('data/csv/raw.csv')
        ctx.send(f"{current_status}")

def run_bot():
    McJohnson.run(token)

run_bot()
