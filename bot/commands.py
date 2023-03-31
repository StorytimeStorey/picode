import discord
import info_parcer as info
import asyncio
import multiprocessing as mp
from alerts import pi_alerts
from discord.ext import tasks
from discord import app_commands
from datetime import datetime

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
channel = client.get_channel(705960640111575061)

@tree.command(name = "print_status", description = "I dont know yet", guild=discord.Object(id=705960639687950387))
async def print_status():
    try:
        current_day = lambda: datetime.today().strftime('%d_%m_%y')
        current_status = info.read_last_row(f'../data/csv/{current_day}_dot.csv')
        channel.send(f"{current_status}")
    except FileNotFoundError:
        channel.send("5-minute file doesn't exist yet. Pulling data from raw...")
        current_status = info.read_last_row('../data/csv/raw.csv')
        channel.send(f"{current_status}")

@tree.command(name = "print_graphs", description = "I dont know yet", guild=discord.Object(id=705960639687950387))
async def print_graphs():
    current_day = lambda: datetime.today().strftime('%d_%m_%y')
    csv_file = f'../data/csv/{current_day}_dot.csv'
    save_location = "data/csv/"
    info.make_graph(csv_file, save_location)
    with open('../data/csv/temperature_and_humidity.png', 'rb') as file:
        image = discord.File(file)
    await channel.send(file=image)
    