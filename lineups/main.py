import os
import discord
import asyncio

from enum import Enum
from dotenv import load_dotenv
from classes.aws import AWS_Connection
from classes.cache import Cache
from classes.selection import Selection
from classes.enums import Nade, Map
from executes import execute_dict

asyncio.set_event_loop(asyncio.new_event_loop())

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Bot()

selection = Selection()

async def set_selected(interaction: discord.Interaction):
    if selection.map is not None and selection.site is not None and selection.side is not None:
        await return_execute(interaction)
        await selection.reset()
    else:
        await interaction.response.defer()

async def return_execute(interaction: discord.Interaction):
    selected_side_description = 'Terrorist' if selection.side == 'T' else 'Counter Terrorist'
    selected_execute = await get_execute(selection.map.name, selection.site, selection.side)

    await interaction.response.send_message(f'Generating {selected_side_description} {selection.site.upper()} Site execute on {selection.map} . . .', delete_after=60)

    execute_emojis = ''
    for key, value in selected_execute.items():
        emoji = ''
        if key.lower() == Nade.Molotov.name.lower():
            fire_emoji = '<:molly:1315925706437296178>'
            for x in range(len(value)):
                emoji += fire_emoji
        elif key.lower() == Nade.Smoke.name.lower():
            smoke_emoji = '<:smoke:1315925707477614613>'
            for x in range(len(value)):
                emoji += smoke_emoji
        else:
            flash_emoji = '<:flash:1315925704998916217>'
            for x in range(len(value)):
                emoji += flash_emoji

        execute_emojis += emoji

    await interaction.followup.send(content=f'{execute_emojis} for {selection.site} site', delete_after=600)
    cache = Cache(os.getenv('CLIP_DIRECTORY'))

    for key, value in selected_execute.items():
        emoji = ''
        if key.lower() == Nade.Molotov.name.lower():
            emoji = '<:molly:1315925706437296178>'
        elif key.lower() == Nade.Smoke.name.lower():
            emoji = '<:smoke:1315925707477614613>'
        else:
            emoji = '<:flash:1315925704998916217>'
        
        for nade in value:
            if len(nade['clip']) > 0:

                aws_connection = AWS_Connection(nade['clip'], selection.map, nade['location'], key)
                clip = await aws_connection.download_clip(cache)
                await interaction.followup.send(content=f'{emoji} for {nade['location']}', file=clip, delete_after=600)
                
            else:
                await interaction.followup.send(f'No Smoke lineup for {selected_side_description} {selection.site.upper()} Site recorded yet. :frowning:', delete_after=600)

    print(f'Cache size utilized: {cache.size} MB')

    if cache.size > 200:
        await cache.evict(200)


class Lineup_View(discord.ui.View):

    map_options = []
    for cs_map in Map:
        map_options.append(discord.SelectOption(label=cs_map.name, value=str(cs_map.value)))

    @discord.ui.select(
        placeholder="Map",
        select_type=discord.ComponentType.string_select,
        row=0,
        min_values=1,
        max_values=1,
        options = map_options
    )
    async def select_callback(self, select, interaction):
        selection.set_map(Map(int(select.values[0])))
        await set_selected(interaction)

    @discord.ui.button(label="Terrorist", row=1, style=discord.ButtonStyle.red)
    async def t_callback(self, button, interaction):
        selection.set_side('T')
        await set_selected(interaction)

    @discord.ui.button(label="Counter Terrorist", row=1, style=discord.ButtonStyle.green)
    async def ct_callback(self, button, interaction):
        selection.set_side('CT')
        await set_selected(interaction)

    @discord.ui.button(label="A Site", row=2, style=discord.ButtonStyle.blurple)
    async def a_site_callback(self, button, interaction):
        selection.set_site('A')
        await set_selected(interaction)

    @discord.ui.button(label="B Site", row=2, style=discord.ButtonStyle.blurple)
    async def b_site_callback(self, button, interaction):
        selection.set_site('B')
        await set_selected(interaction)

    @discord.ui.button(label="Mid Site", row=2, style=discord.ButtonStyle.blurple)
    async def mid_site_callback(self, button, interaction):
        selection.set_site('Mid')
        await set_selected(interaction)


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(description='Sends an execute for the popular fps game Counter Strike!!!!!')
async def execute(ctx):
    await ctx.respond("You still a crackr! ", view=Lineup_View(), delete_after=600)

@bot.command()
async def clear_history(ctx):
    channel = bot.get_channel(ctx.channel.id)
    messages = await channel.history(limit=500).flatten()

    await ctx.respond('Clearing messages. . .', delete_after=300)
    index = 1
    for message in messages:
        await message.delete()
        print(f'Message {index} deleted')
        index += 1
        

async def get_execute(map, site, side):
    return execute_dict[map][side][site]
        

bot.run(TOKEN)