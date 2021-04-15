import asyncio
import discord
from discord.ext import commands
import requests
from datetime import datetime
import json
import os
from randomcolor import RandomColor

TOKEN = os.environ.get('TOKEN')

bot = commands.Bot(command_prefix='m!',
                   description='''ToyaMine''')

def createCords(coords, user):
    date = datetime.now()
    return {"Coordinates":f"{coords}", "User":f"{user}", "Date":f"{date.strftime('%x')}"}

async def checkPlayer():
    while True:
        r = requests.get("https://mcapi.us/server/status?ip=office.toyaga.eu")
        r = r.json()
        players = r["players"]["sample"]
        print(players)
        await asyncio.sleep(600)

        r = requests.get("https://mcapi.us/server/status?ip=office.toyaga.eu")
        r = r.json()
        print(r["players"]["sample"])
        for i in r["players"]["sample"]:
            if i not in players:
                channel = bot.get_channel(829796491395989565)
                em = discord.Embed(title=f"{i['name']} has just connected!", colour=discord.Colour(0x00ff00))
                em.set_thumbnail(url=f"https://crafatar.com/avatars/{i['id']}")
                em.set_author(name="MineToy", url="https://toyaga.eu", icon_url="https://static.wikia.nocookie.net/minecraft/images/b/b0/Stick_inventory.png/revision/latest/scale-to-width-down/150?cb=20110823193610")
                await channel.send(embed=em)
                

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.loop.create_task(checkPlayer())

@bot.command()
async def coords(ctx,mode="all", *, coords=None,):
    """"Add/List/Delete coordinates of places in the Toyaga minecraft server"""


    if mode == "all":
        with open("coords.json", "r") as f:
            our_coords = json.load(f)
            our_coords = our_coords["coords"]
        randoCol = RandomColor()
        randoCol = randoCol.generate()
        randoCol = randoCol[0].replace("#", "")
        randoCol = int(randoCol, 16)

        em = discord.Embed(title=f"Coordinate Compass", colour=discord.Colour(randoCol))
        em.set_thumbnail(url="https://www.pngkit.com/png/full/206-2062034_minecraft-bukkit-icon-8-bit-coin.png")
        em.set_author(name="MineToy", url="https://toyaga.eu", icon_url="https://static.wikia.nocookie.net/minecraft/images/b/b0/Stick_inventory.png/revision/latest/scale-to-width-down/150?cb=20110823193610")

        for i in range(len(our_coords)):
            i = our_coords[i]
            em.add_field(name=f"{i['Coordinates']}", value=f"Coords set by: {i['User']}, on {i['Date']}", inline=False)
        em.set_footer(text=f"Command ran on: {datetime.now()}")
        await ctx.send(embed=em)


    elif mode == "add":
        if coords:
            with open("coords.json","r+") as f:
                data = json.load(f)
                temp = data["coords"]
                temp.append(createCords(coords, ctx.message.author.name))
                f.seek(0)
                json.dump(data, f)
                await ctx.message.add_reaction("✅")

        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("Give me coords!!!")

    elif mode == "del":
        data = None
        with open("coords.json", "r") as f:
            data = json.load(f)

        if not data or "coords" not in data:
            return await ctx.send("Error: No coords available")

        with open("coords.json", "w") as f:
            data["coords"] = data["coords"][:-1]
            # temp = data["coords"]
            # temp.pop()
            # f.seek(0)
            json.dump(data, f)
            await ctx.message.add_reaction("✅")

    elif mode == "help":
        await ctx.send("To add new coords use this example syntax: `m!coords add My house: -31, 53, 120`\nTo remove last coordinate entry do: `m!coords del`\nTo list all the different coords type in: `m!coords`, or `m!coords all`")
    else:
        await ctx.send("Invalid use, please use this syntax:\n`m!coords add/all/del`\nFor more help please type in `m!coords help`")


@bot.command()
async def status(ctx):
    """| Get status on the Toyaga server"""
    r = requests.get("https://mcapi.us/server/status?ip=office.toyaga.eu")
    r = r.json()
    status, players = r["status"], r["players"]
    em = discord.Embed(title=f"Info about office.toyaga.eu", colour=discord.Colour(0x8c0303))
    em.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft/images/b/b0/Stick_inventory.png/revision/latest/scale-to-width-down/150?cb=20110823193610")
    em.set_author(name="MineToy", url="https://toyaga.eu", icon_url="https://static.wikia.nocookie.net/minecraft/images/b/b0/Stick_inventory.png/revision/latest/scale-to-width-down/150?cb=20110823193610")
    if status == "success":
        em.add_field(name="Status", value=f"Server is up!", inline=False)
    else:
        em.add_field(name="Status", value="Server is down :C .",  inline=False)
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
