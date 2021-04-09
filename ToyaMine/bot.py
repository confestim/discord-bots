import asyncio
import discord
from discord.ext import commands
from config import TOKEN
import requests

bot = commands.Bot(command_prefix='m!',
                   description='''ToyaMine''')

@bot.command()
async def status(ctx):
    """| Get status on the toyaga server"""
    r = requests.get("https://mcapi.us/server/status?ip=office.toyaga.eu")
    r = r.json()
    status, players = r["status"], r["players"]
    em = discord.Embed(title=f"Info about office.toyaga.eu", colour=discord.Colour(0x8c0303))
    if status == "success":
        em.add_field(name="Status", value=f"Online", inline=False)
    else:
        em.add_field(name="Status", value="Not online",  inline=False)
    if players['now'] == "0":
        em.set_footer(text="There are no players online")
    else:
        counter = 0
        for i in players["sample"]:
            counter += 1
            em.add_field(name=f"Player {counter}", value=i["name"])
        if players['now'] == 1:
            em.set_footer(text=f"There is 1 player online")
        else:
            em.set_footer(text=f"There are {players['now']} players online")
    await ctx.send(embed=em)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(bot.start(TOKEN))
except KeyboardInterrupt:
    loop.run_until_complete(bot.logout())
finally:
    loop.close()
