import os
import discord
import asyncio

from executes import execute_dict
from discord import ui
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

selected_map = ''
selected_site = ''
selected_side = ''

async def print_selected():
    print(f'Map: {selected_map}')
    print(f'Site: {selected_site}')
    print(f'Side: {selected_side}')

async def set_selected(interaction: discord.Interaction):
    if len(selected_map) > 0 and len(selected_site) > 0 and len(selected_side) > 0:
        await return_execute(interaction)
    else:
        await interaction.response.defer()

async def return_execute(interaction: discord.Interaction):
    selected_side_description = 'Terrorist' if selected_side == 't' else 'Counter Terrorist'
    selectedExecute = get_execute(selected_map, selected_site, selected_side)

    await interaction.message.delete()
    await interaction.response.send_message(f'Generating {selected_side_description} {selected_site.upper()} Site execute on {selected_map} . . .', delete_after=890)
    
    for key, value in selectedExecute.items():
        if len(value['clip']) > 0:
            with open(value['clip'], 'rb') as file:
                await interaction.followup.send(content=f'{key} for {value['location']} on {selected_site.upper()} site', file=discord.File(file, 'file.gif'), delete_after=890)
        else:
            await interaction.followup.send(f'No {key} lineup for {selected_side_description} {selected_site.upper()} Site recorded yet. :frowning:', delete_after=890)

class MyView(discord.ui.View):

    @discord.ui.select(
        placeholder="Map", 
        row=0,
        options = [
            discord.SelectOption(label="Anubis", value="Anubis"),
            discord.SelectOption(label="Ancient", value="Ancient"),
            discord.SelectOption(label="Dust2", value="Dust2"),
            discord.SelectOption(label="Inferno", value="Inferno"),
            discord.SelectOption(label="Mirage", value="Mirage"),
            discord.SelectOption(label="Nuke", value="Nuke"),
            discord.SelectOption(label="Vertigo", value="Vertigo")
        ]
    )
    async def select_callback(self, select, interaction):
        global selected_map
        selected_map = select.values[0]
        await set_selected(interaction)

    @discord.ui.button(label="A Site", row=1, style=discord.ButtonStyle.blurple)
    async def a_site_callback(self, button, interaction):
        global selected_site
        selected_site = 'a'
        await set_selected(interaction)

    @discord.ui.button(label="B Site", row=1, style=discord.ButtonStyle.blurple)
    async def b_site_callback(self, button, interaction):
        global selected_site
        selected_site = 'b'
        await set_selected(interaction)

    @discord.ui.button(label="Mid Site", row=1, style=discord.ButtonStyle.blurple)
    async def mid_site_callback(self, button, interaction):
        global selected_site
        selected_site = 'mid'
        await set_selected(interaction)

    @discord.ui.button(label="Terrorist", row=2, style=discord.ButtonStyle.red)
    async def t_callback(self, button, interaction):
        global selected_side
        selected_side = 't'
        await set_selected(interaction)

    @discord.ui.button(label="Counter Terrorist", row=2, style=discord.ButtonStyle.green)
    async def ct_callback(self, button, interaction):
        global selected_side
        selected_side = 'ct'
        await set_selected(interaction)


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.command()
async def execute(ctx):
    await ctx.send(f"You still a crackr! ", view=MyView(), delete_after=890)
    await ctx.message.delete()

@bot.command()
async def clear_history(ctx):
    channel = bot.get_channel(ctx.channel.id)
    messages = await channel.history(limit=500).flatten()

    await ctx.send('Clearing messages. . .', delete_after=300)
    index = 1
    for message in messages:
        await message.delete()
        print(f'Message {index} deleted')
        index += 1
        

def get_execute(map, site, side):
    return execute_dict[map][side][site]
        

bot.run(TOKEN)