import os
import discord
import cache

from executes import execute_dict
from dotenv import load_dotenv
from aws import download_clip

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#intents = discord.Intents.all()
bot = discord.Bot(intents=discord.Intents.all())

selected_map = ''
selected_site = ''
selected_side = ''

async def reset_selected():
    global selected_map
    selected_map = ''

    global selected_site
    selected_site = ''

    global selected_side
    selected_side = ''

async def set_selected(interaction: discord.Interaction):
    if len(selected_map) > 0 and len(selected_site) > 0 and len(selected_side) > 0:
        await return_execute(interaction)
        await reset_selected()
    else:
        await interaction.response.defer()

async def return_execute(interaction: discord.Interaction):
    selected_side_description = 'Terrorist' if selected_side == 'T' else 'Counter Terrorist'
    selectedExecute = get_execute(selected_map, selected_site, selected_side)

    await interaction.response.send_message(f'Generating {selected_side_description} {selected_site.upper()} Site execute on {selected_map} . . .', delete_after=60)
    
    for key, value in selectedExecute.items():
        emoji = ''
        if key.lower() == 'mollies':
            emoji = ':fire:'
        elif key.lower() == 'smokes':
            emoji = ':cloud:'
        else:
            emoji = ':flashlight:'

        emoji_group = ''
        for x in range(len(value)):
            emoji_group += emoji
        
        await interaction.followup.send(content=f'{emoji_group} for {selected_site} site', delete_after=600)
        
        for nade in value:
            if len(nade['clip']) > 0:

                clip = await download_clip(nade['clip'], selected_map, nade['location'], key)
                await interaction.followup.send(content=f'{emoji} for {nade['location']}', file=clip, delete_after=600)
                
            else:
                await interaction.followup.send(f'No Smoke lineup for {selected_side_description} {selected_site.upper()} Site recorded yet. :frowning:', delete_after=600)

        utilized_cache = cache.check_size('clips')
        print(f'Cache size utilized: {utilized_cache} MB')

        if utilized_cache > 200:
            cache.evict(200)


class MyView(discord.ui.View):

    @discord.ui.select(
        placeholder="Map", 
        row=0,
        options = [
            discord.SelectOption(label="Ancient", value="Ancient"),
            discord.SelectOption(label="Anubis", value="Anubis"),
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
        selected_site = 'A'
        await set_selected(interaction)

    @discord.ui.button(label="B Site", row=1, style=discord.ButtonStyle.blurple)
    async def b_site_callback(self, button, interaction):
        global selected_site
        selected_site = 'B'
        await set_selected(interaction)

    @discord.ui.button(label="Mid Site", row=1, style=discord.ButtonStyle.blurple)
    async def mid_site_callback(self, button, interaction):
        global selected_site
        selected_site = 'Mid'
        await set_selected(interaction)

    @discord.ui.button(label="Terrorist", row=2, style=discord.ButtonStyle.red)
    async def t_callback(self, button, interaction):
        global selected_side
        selected_side = 'T'
        await set_selected(interaction)

    @discord.ui.button(label="Counter Terrorist", row=2, style=discord.ButtonStyle.green)
    async def ct_callback(self, button, interaction):
        global selected_side
        selected_side = 'CT'
        await set_selected(interaction)


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(description='Sends an execute for the popular fps game Counter Strike!!!!!')
async def execute(ctx):
    await ctx.respond(f"You still a crackr! ", view=MyView(), delete_after=600)

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
        

def get_execute(map, site, side):
    return execute_dict[map][side][site]
        

bot.run(TOKEN)