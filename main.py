import os
import discord

from discord import ui
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


maps = {'anubis', 'ancient', 'dust2', 'inferno', 'mirage', 'nuke', 'vertigo'}
sites = {'a', 'b', 'mid'}

executedict = {
    "anubis": {
        "t": {
            "a": {
                "smoke1" : "https://csnades.gg/anubis/smokes/heaven-from-t-upper",
                "smoke2" : "https://csnades.gg/anubis/smokes/platform-from-water",
                "smoke3" : "https://csnades.gg/anubis/smokes/connector-from-t-upper",
                "molly" : "https://csnades.gg/anubis/molotovs/a-site-from-water",
                "flash" : "https://csnades.gg/anubis/flashbangs/a-site-from-water"
            },
            "b": {
                "smoke1" : "https://csnades.gg/anubis/smokes/b-site-from-ruins-d",
                "smoke2" : "https://csnades.gg/anubis/smokes/temple-from-ruins-b",
                "smoke3" : "https://csnades.gg/anubis/smokes/ebox-from-ruins-b",
                "molly" : "https://csnades.gg/anubis/molotovs/b-pillar-from-ruins-b",
                "flash" : "https://csnades.gg/anubis/flashbangs/b-site-from-ruins"
            },
            "mid": {
                "smoke1" : "https://csnades.gg/anubis/smokes/top-mid-from-t-spawn-b",
                "smoke2" : "https://csnades.gg/anubis/smokes/canals-from-t-spawn-b",
                "smoke3" : "https://csnades.gg/anubis/smokes/mid-b-door-from-street",
                "molly" : "https://csnades.gg/anubis/molotovs/mid-doors-from-bridge",
                "flash" : "https://csnades.gg/anubis/flashbangs/bridge-from-ruins",
            }
        }
    },
    "mirage": {
        "t": {
            "a": {
                "smoke1" : "https://csnades.gg/mirage/smokes/jungle-from-a-ramp",
                "smoke2" : "https://csnades.gg/mirage/smokes/top-of-ticket-booth-from-a-ramp",
                "smoke3" : "https://csnades.gg/mirage/smokes/stairs-from-a-ramp",
                "molly" : "https://csnades.gg/mirage/molotovs/dark-from-palace-safe",
                "flash" : "https://csnades.gg/mirage/flashbangs/a-ramp-from-a-ramp"
            },
            "b": {
                "smoke1" : "https://csnades.gg/mirage/smokes/market-door-from-back-alley",
                "smoke2" : "https://csnades.gg/mirage/smokes/market-window-from-back-alley",
                "smoke3" : "https://csnades.gg/mirage/smokes/right-arch-from-back-alley",
                "molly" : "https://csnades.gg/mirage/molotovs/bench-from-b-apts",
                "flash" : "https://csnades.gg/mirage/flashbangs/b-site-from-back-apts"
            },
            "mid": {
                "smoke1" : "https://csnades.gg/mirage/smokes/market-door-from-back-alley",
                "smoke2" : "https://csnades.gg/mirage/smokes/market-window-from-back-alley",
                "smoke3" : "https://csnades.gg/mirage/smokes/right-arch-from-back-alley",
                "molly" : "https://csnades.gg/mirage/flashbangs/b-site-from-back-apts",
                "flash" : "https://csnades.gg/mirage/flashbangs/b-site-from-back-apts",
            }
        }
    }
}




@bot.command()
async def execute(ctx):

    mapSelect = ui.Select(placeholder="Map", options=[
        discord.SelectOption(label="Anubis", value="anubis"),
        discord.SelectOption(label="Ancient", value="ancient"),
        discord.SelectOption(label="Dust2", value="dust2"),
        discord.SelectOption(label="Inferno", value="inferno"),
        discord.SelectOption(label="Mirage", value="mirage"),
        discord.SelectOption(label="Nuke", value="nuke"),
        discord.SelectOption(label="Vertigo", value="vertigo")
    ])

    siteSelect = ui.Select(placeholder="Site", options = [
        discord.SelectOption(label="A Site", value="a"),
        discord.SelectOption(label="B Site", value="b"),
        discord.SelectOption(label="Mid", value="mid"),
    ])

    sideSelect = ui.Select(placeholder="Side", options = [
        discord.SelectOption(label="T Side", value="t"),
        discord.SelectOption(label="CT Side", value="ct")
    ])

    async def select_callback(interaction: discord.Interaction):
        if not mapSelect.values or not siteSelect.values or not sideSelect.values:
            await interaction.response.defer()
        else:
            selectedExecute = get_execute(mapSelect.values[0], siteSelect.values[0], sideSelect.values[0])
            print(selectedExecute)
            await interaction.response.send_message(selectedExecute['smoke1'])
            await interaction.followup.send(selectedExecute['smoke2'])
            await interaction.followup.send(selectedExecute['smoke3'])
            await interaction.followup.send(selectedExecute['molly'])
            await interaction.followup.send(selectedExecute['flash'])

    mapSelect.callback = select_callback
    siteSelect.callback = select_callback
    sideSelect.callback = select_callback

    view = ui.View()
    view.add_item(mapSelect)
    view.add_item(siteSelect)
    view.add_item(sideSelect)

    await ctx.send("You're such a cracker!", view=view)


def get_execute(map, site, side):
    return executedict[map][side][site]
        

bot.run(TOKEN)