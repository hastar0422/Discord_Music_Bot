"""
作品名稱     : Discord Music Bot
__author__ : Ning甯詠城
"""
#參考 ：https://python.land/build-discord-bot-in-python-that-plays-music
import itertools

import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import youtube_dl
import asyncio
import time
from threading import Timer
import warnings

warnings.filterwarnings("ignore")
load_dotenv()
# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("discord_token")
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
youtube_dl.utils.bug_reports_message = lambda: ''

str_music=[]
queue_url=[]
song=[]
stopmusic = []
playmusic = "readytoplay"
URL = []
timedelay = []
timeclock = 0
control = 1
@bot.command(name='Play', help='To play song')
async def Play(ctx, url):                                       #ctx是一種引數，且ctx是context(上下文的縮寫)

    try:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    except:
        pass

    try:
        async with ctx.typing():
            server = ctx.message.guild
            voice_client = ctx.message.guild.voice_client
            queue_url.append(url)
            ydl_opts = {'format': 'bestaudio'}  # 這行開始不用下載
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(queue_url.pop(0), download=False)
                print("check is playing")
                URL.append(info['formats'][0]['url'])
                timedelay.append(info['duration'])
                time.sleep(2)
                #playerstop(server, voice_client)
                print("go test")
                await test(control, server, voice_client)
                """try:

                    if  (voice_client.is_playing()==False):
                        playerstop(server,voice_client)
                except:
                    pass

                finally:
                    if URL != []:
                        URL.pop(0)
                        print("URL != [")
                        time.sleep(int(timedelay.pop(0)) + 2)
                        print("sleep")
                        playerstop(server, voice_client)
                        playmusic = "readytoplay"
                        playsong(server, playmusic, voice_client)"""





                """elif len(timedelay) != 0 and len(URL)==len(timedelay)-1:
                    time.sleep(timedelay.pop(0) + 1)
                    playerstop(server, voice_client)"""

    except:
        print("The bot is not connected to a voice channel.")

async def test(control,server,voice_client):
    print("in test")

    if control==1:
        x = 0
        while x < 30000:
            if voice_client.is_playing():
                #print("is playing")
                await asyncio.sleep(3.2)
                #print("wake asyncio")
                x = x + 1
            else:
                playerstop(server, voice_client)
    elif voice_client.is_paused():
        x = 0
        while x < 30000:
            await asyncio.sleep(2.2)
            x = x + 1

def playerstop(server,voice_client):
    #voice_client = ctx.message.guild.voice_client
    #if voice_client.is_playing():
    #    if URL!=[]:
    #        asyncio.sleep(timedelay.pop(0)+1)
    #        playerstop(ctx)

    if playmusic == "readytoplay":
        playsong(server, playmusic, voice_client)

    """if voice_client.is_playing():
        x = 0
        while x < 30000:
            if voice_client.is_playing():
                print("is playing")
                time.sleep(2.2)
                print("wake asyncio")
                x = x + 1
            else:
                playerstop(server,voice_client)



    else:
        playmusic = "readytoplay"""
        #playsong(server, playmusic, voice_client)




def playsong(server,playmusic,voice_client):
    #server = ctx.message.guild
    voice_channel = server.voice_client
    if playmusic == "readytoplay":
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}
            voice_channel.play(discord.FFmpegPCMAudio(URL.pop(0), **FFMPEG_OPTIONS))

            if len(URL) > 0:
                test(control,server,voice_client)

            #voice_channel.timeout(int(timedelay[0])+1)


    elif playmusic == "playnextsong":

        playmusic = "readytoplay"
        playsong(server,playmusic,voice_client)



"""def queue(url):
    queue_url.append(url)
    return queue_url"""


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_client = ctx.message.guild.voice_client
    voice_client.pause()
    control = 0
    await test(control,server,voice_client)
    print("pause")


@bot.command(name='next', help='This command play next song')
async def next(ctx):
    server = ctx.message.guild
    voice_client = ctx.message.guild.voice_client
    voice_client.pause()
    await test(control, server, voice_client)
    #playmusic = "playnextsong"
    #playsong(ctx,playmusic)

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.event
async def on_ready():
    print('Running!')

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)