import discord
import asyncio
from discord.ext import commands
from config import TOKEN
from time import sleep

bot = commands.Bot(command_prefix='&',
                   description='''multi-tool bot made by Yamozha''')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    game = discord.Game("&help")
    await bot.change_presence(activity=game, status=discord.Status.dnd)

@bot.command()
async def timer(ctx, timer_time):
    if not timer_time:
        return await ctx.send("Please specify time!\n`&timer 3h`")    

    if "h" in timer_time:
        time = int(timer_time.strip("h")) * 3600
    elif "m" in timer_time:
        time = int(timer_time.strip("m")) * 60
    elif "s" in timer_time:
        time = int(timer_time.strip("s"))
    else:
        ctx.send("Try formatting it better!!")
    await ctx.message.add_reaction("✔️")
    await asyncio.sleep(time)
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio("./alarm.mp3"))
    while vc.is_playing():
        await sleep(1)
    await vc.disconnect()

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(bot.start(TOKEN))
except KeyboardInterrupt:
    loop.run_until_complete(bot.logout())
finally:
    loop.close()
