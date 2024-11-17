import os
import discord

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user}has connected to Discord!')

@client.event
async def on_message(message):
    if message.content == 'mirage b attack':
        await message.channel.send('https://csnades.gg/mirage/smokes/market-door-from-back-alley')
        await message.channel.send('https://csnades.gg/mirage/smokes/market-window-from-back-alley')
        await message.channel.send('https://csnades.gg/mirage/smokes/right-arch-from-back-alley')
        await message.channel.send('https://csnades.gg/mirage/flashbangs/b-site-from-back-apts')
        await message.channel.send('https://csnades.gg/mirage/flashbangs/b-site-from-back-apts')

client.run(TOKEN)