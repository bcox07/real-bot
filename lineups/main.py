import os
import json
import discord
import asyncio

from enum import Enum
from dotenv import load_dotenv
from classes.aws import AWS_Connection, S3_Client, DynamdDB_Client
from classes.cache import Cache
from classes.selection import Selection
from classes.enums import Nade, Map
from executes import execute_dict

asyncio.set_event_loop(asyncio.new_event_loop())

load_dotenv()
bot = discord.Bot()

selection = Selection()

AWS_SECRET_STRING = json.loads(os.getenv('AWS_SECRET'))
AWS_ACCESS_KEY = AWS_SECRET_STRING['S3_ACCESS_KEY']
AWS_SECRET_KEY = AWS_SECRET_STRING['S3_SECRET_KEY']
REGION_NAME = os.getenv('AWS_REGION')
TOKEN = json.loads(os.getenv('DISCORD_TOKEN'))['DISCORD_TOKEN']
print(TOKEN)

s3_connection = AWS_Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME, 's3')
dynamodb_connection = AWS_Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME, 'dynamodb')

async def set_selected(interaction: discord.Interaction):
    if selection.map is not None and selection.site is not None and selection.side is not None:
        await return_execute(interaction)
        await selection.reset()
    else:
        await interaction.response.defer()

def get_execute_emoji(nade):
    fire_emoji = '<:molly:1315925706437296178>'
    smoke_emoji = '<:smoke:1315925707477614613>'
    flash_emoji = '<:flash:1315925704998916217>'

    print(f'Nade name: {nade.get('S').upper()}')

    if nade.get('S').upper() == Nade.Molotov.name.upper():
        return fire_emoji
    elif nade.get('S').upper() == Nade.Smoke.name.upper():
        return smoke_emoji
    elif nade.get('S').upper() == Nade.Flash.name.upper():
        return flash_emoji
    else:
        print('Invalid nade submitted for emoji')
        return flash_emoji

def get_execute_emojis(selected_execute):
    execute_emojis = ''
    for index in selected_execute:
        nade_emoji = get_execute_emoji(index.get('Type'))
        execute_emojis += nade_emoji             

    return execute_emojis

async def return_execute_from_command(ctx, map: Map, side: str, site: str):
    selected_side_description = 'Terrorist' if side == 'T' else 'Counter Terrorist'
    print(f'Map: {map.name}')
    print(f'Site: {site}')
    print(f'Side: {side}')

    selected_execute = await get_execute(map.name, site, side)

    await ctx.respond(f'Generating {selected_side_description} {site} Site execute on {map.name} . . .', delete_after=60)
    await ctx.respond(content=f'{get_execute_emojis(selected_execute)} for {site} site', delete_after=600)

    cache = Cache(os.getenv('CLIP_DIRECTORY'))
    for key, value in selected_execute.items():
        emoji = get_execute_emoji(key)
        
        for nade in value:
            if len(nade['clip']) > 0:
                s3_client = S3_Client(s3_connection.client, nade['clip'], map, nade['location'], key)
                clip = await s3_client.download_clip(cache)
                await ctx.respond(content=f'{emoji} for {nade['location']}', file=clip, delete_after=600)
                
            else:
                await ctx.respond(f'No Smoke lineup for {selected_side_description} {site} Site recorded yet. :frowning:', delete_after=600)

async def return_execute(interaction: discord.Interaction):
    selected_side_description = 'Terrorist' if selection.side == 'T' else 'Counter Terrorist'
    dynamodb_client = DynamdDB_Client(dynamodb_connection.client, 'Lineups')
    selected_execute = await dynamodb_client.get_lineups(selection.map.name, selection.side, selection.site)
    #selected_execute = await get_execute(selection.map.name, selection.site, selection.side)

    print(selected_execute.items())
    await interaction.response.send_message(f'Generating {selected_side_description} {selection.site.upper()} Site execute on {selection.map.name} . . .', delete_after=60)
    await interaction.followup.send(content=f'{get_execute_emojis(selected_execute.get('Items'))} for {selection.site} site', delete_after=600)

    cache = Cache(os.getenv('CLIP_DIRECTORY'))
    for value in selected_execute.get('Items'):
        emoji = get_execute_emoji(value.get('Type'))
        
        if len(value.get('URI')) > 0:
            s3_client = S3_Client(
                s3_connection.client,
                value.get('URI')['S'],
                selection.map,
                value.get('Location')['S'],
                value.get('Type')['S'])
            clip = await s3_client.download_clip(cache)

            try:
                await interaction.followup.send(content=f'{emoji} for {value.get('Location')['S']}', file=clip, delete_after=600)
            except Exception as e:
                #await interaction.followup.send('There was an issue attempting to send this clip. Wiwiwi', delete_after=600)
                print(e)
            
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

async def get_maps(ctx: discord.AutocompleteContext):
    return [map.name for map in Map]

async def get_sides(ctx: discord.AutocompleteContext):
    return ['T', 'CT']

async def get_sites(ctx: discord.AutocompleteContext):
    return ['A', 'B', 'Mid']

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.command(description='Request a lineup')
async def lineup(
    ctx,
    map: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_maps)),
    side: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_sides)),
    site: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_sites)),
):
    await return_execute_from_command(ctx, Map[map], side, site)

@bot.slash_command(description='Provides a UI for requesting a lineup')
async def lineup_ui(ctx):
    await ctx.respond("What lineups do you want to learn?", view=Lineup_View(), delete_after=600)

#@bot.command(description='Stores a clip to possibly be used in the lineup request')
#async def add_clip(ctx, map: str, team: str, site: str):

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