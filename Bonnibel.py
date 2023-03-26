import discord
import bot.info_parcer as info
import asyncio

# class BonnibelBot:
#     def __init__(self, token):
#         self.intents = discord.Intents.default()
#         self.intents.message_content = True
#         self.client = discord.Client(intents=self.intents)
#         self.token = token


#     @client.event
#     async def on_read(self):
#         print(f"We have logged in as {self.client.user}")

#     @client.event
#     async def on_message(self, message):
#         if message.author == self.client.user:
#             return

#         if message.content.startswith('$hello'):
#             await message.channel.send("hello!")

#         if message.content.startswith('$status'):
#             current_status = info.read_last_row('../data/csv/dot.csv')
#             await message.channel.send(f"{current_status}")

#         if message.content.startswith("$graph"):
#             info.make_graph()
#             with open('../data/csv/temperature_and_humidity.png', 'rb') as file:
#                 image = discord.File(file)
#             await message.channel.send(file=image)

#     @client.event
#     async def run(self):
#         asyncio.create_task(self.on_read())
#         #self.client.add_listener(self.on_message)
#         await self.client.start(self.token)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_read():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send("hello!")

    if message.content.startswith('$status'):
        current_status = info.read_last_row('data/csv/dot.csv')
        await message.channel.send(f"{current_status}")

    if message.content.startswith("$graph"):
        csv_file = "data/csv/dot.csv"
        save_location = "data/csv/"
        info.make_graph(csv_file, save_location)
        with open('data/csv/temperature_and_humidity.png', 'rb') as file:
            image = discord.File(file)
        await message.channel.send(file=image)

with open('../token.txt') as f: token = f.read().strip()
client.run(f"{token}")

# if __name__ == "__main__":
#     with open('C:/Users/tomic/Desktop/token.txt') as f: token = f.read().strip()
#     bot = BonnibelBot(f'{token}')
#     asyncio.run(bot.run())
