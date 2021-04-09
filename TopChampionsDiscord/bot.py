import discord
import asyncio
from discord.ext import commands
import youtube_dl
import os, glob, sys, re
from youtube_search import YoutubeSearch
import TenGiphPy

g = TenGiphPy.Giphy(token='token for giphy')# yes i accidentally leaked mine here but it has been reset
TOKEN = "token id here" # here too
bot = commands.Bot(command_prefix='#',
                   description='''multi-tool bot made by Yamozha''')

queue = []

def youtubeDown(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloadedsongs/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)


    if ".webm" in filename:
        filename = filename.replace(".webm", ".mp3")
    elif ".mp4" in filename:
        filename = filename.replace(".mp4", ".mp3")
    elif ".m4a" in filename:
        filename = filename.replace(".m4a", ".mp3")

    return filename


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    game = discord.Game("#help")
    await bot.change_presence(activity=game, status=discord.Status.dnd)

@bot.command(aliases=["sus","drip"])
async def amongus(ctx):
    em = discord.Embed(colour=discord.Colour(0xFF0000))
    em.set_image(url=f"{g.random(tag='amongus')['data']['images']['downsized_large']['url']}")

    return await ctx.send(embed=em)


@bot.command()
async def ping(ctx):
    """ Pong """
    await ctx.send("pong")


@bot.command()
async def top3league(ctx, username=None, region=None):
    """| Checks your top 3 champions in league"""

    # Check if user has provided username
    if not username:
        await ctx.send("Please give me a LoL username")
        await ctx.send("`usage: #top3league username region`")
        return

    # If user provides info as input, print information about the command
    elif not region:
        await ctx.send("Please give me a LoL region")
        await ctx.send("`usage: #top3league username region`")

    else:

        # Check if the account exists or not


        em = discord.Embed(title=f"{username}'s top 3")
        em.set_image(url=f"https://www.masterypoints.com/image/profile/{username}/{region}")

        return await ctx.send(embed=em)

@bot.command(aliases=["p","paly"])
async def play(ctx, *, url):
    """| Plays a song or adds it to queue"""
    print(url)
    print(str(url))
    is_url = re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", url)
    if is_url:
        print("it's an url!")

        if "www" in url:
            url_thumbnail = url.replace("https://www.youtube.com/watch?v=",
                                        "http://i3.ytimg.com/vi/") + "/maxresdefault.jpg"
        else:
            url_thumbnail = url.replace("https://youtube.com/watch?v=",
                                        "http://i3.ytimg.com/vi/") + "/maxresdefault.jpg"

        print(url_thumbnail)

        pass
    else:
        url_dict = YoutubeSearch(url, max_results=1).to_dict()
        print(url_dict)
        url = f"https://youtube.com/{url_dict[0]['url_suffix']}"

    files = glob.glob("downloadedsongs/*")
    if len(files) > 10:
        for i in files:
            os.remove(i)

    print(len(files))

    channel = ctx.author.voice.channel
    try:
        vc = await channel.connect()

    except Exception as e:
        vc = ctx.message.guild.voice_client
        print(e)
        pass

    if vc.is_playing():
        queue.append(url)

        if not is_url:
            em = discord.Embed(title=f"Added {url_dict[0]['title']} to queue", colour=discord.Colour(0x8c0303))
            em.set_image(url=url_dict[0]['thumbnails'][0])
            em.add_field(name=f"{url_dict[0]['channel']}", value=f"{url_dict[0]['views']}", inline=False)
            await ctx.send(embed=em)

        else:
            with youtube_dl.YoutubeDL() as ydl:
                object = ydl.extract_info(url, download=False)
                print(object["title"])
            em = discord.Embed(title=f"Added {object['title']} to queue", colour=discord.Colour(0x8c0303))
            em.set_image(url=url_thumbnail)
            await ctx.send(embed=em)


            # em = discord.Embed(title/

    elif not vc.is_playing() and len(queue) == 0:

        player = vc.play(discord.FFmpegPCMAudio(f"{youtubeDown(url)}"))

        if not is_url:
            em = discord.Embed(title=f"Playing {url_dict[0]['title']}", colour=discord.Colour(0x8c0303))
            em.set_image(url=url_dict[0]['thumbnails'][0])
            em.add_field(name=f"{url_dict[0]['channel']}",value=f"{url_dict[0]['views']}", inline=False)
            await ctx.send(embed=em)

        else:
            with youtube_dl.YoutubeDL() as ydl:
                object = ydl.extract_info(url, download=False)
            print(object["title"])
            em = discord.Embed(title=f"Playing {object['title']} ", colour = discord.Colour(0x8c0303))
            em.set_image(url=url_thumbnail)
            await ctx.send(embed=em)

    return


@bot.command(aliases=["s","sikp"])
async def skip(ctx):
    """| Skip song"""

    channel = ctx.author.voice.channel
    try:
        vc = await channel.connect()
    except Exception as e:
        vc = ctx.message.guild.voice_client
        print(e)
        pass

    if vc.is_playing() and len(queue) != 0:
        vc.stop()
        print(queue)
        url  = queue[0]

        if "www" in url:
            url_thumbnail = url.replace("https://www.youtube.com/watch?v=", "http://i3.ytimg.com/vi/") + "/maxresdefault.jpg"
        else:
            url_thumbnail = url.replace("https://youtube.com//watch?v=",
                                        "http://i3.ytimg.com/vi/") + "/maxresdefault.jpg"

        with youtube_dl.YoutubeDL() as ydl:
            object = ydl.extract_info(url, download=False)

        print(object["title"])

        em = discord.Embed(title=f"Playing {object['title']} ", colour=discord.Colour(0x8c0303))
        em.set_image(url=url_thumbnail)
        await ctx.send(embed=em)

        player = vc.play(discord.FFmpegPCMAudio(f"{youtubeDown(url)}"))
        queue.pop(0)


@bot.command(aliases=["queue","que"])
async def q(ctx):
    """| Show queue"""
    em = discord.Embed(title=f"Queue")
    number = 0
    for i in queue:
        number += 1
        em.add_field(name=f"{number}.", value=i, inline=False)
    await ctx.send(embed=em)

@bot.command(aliases=["l","begai"])
async def leave(ctx):
    """ | Makes the bot leave the voice channel its in"""
    server = ctx.message.guild.voice_client
    return await server.disconnect()

@bot.command()
async def stop(ctx):
    """| Stop current song """
    server = ctx.message.guild.voice_client
    return await server.stop()

@bot.command()
async def dababy(ctx):
    """| Dababy """

    em = discord.Embed(title=f"🚗 🚗 🚗")
    em.set_image(url=f"{g.random(tag='dababy')['data']['images']['downsized_large']['url']}")
    await ctx.send(embed=em)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(bot.start(TOKEN))
except KeyboardInterrupt:
    loop.run_until_complete(bot.logout())
finally:
    loop.close()
