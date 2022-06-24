"""
作品名稱     : Discord Music Bot
__author__ : Ning甯詠城
"""
#參考 ：https://python.land/build-discord-bot-in-python-that-plays-music
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import youtube_dl
import asyncio
import time
import warnings
warnings.filterwarnings("ignore")
load_dotenv()
# Get the API token from the .env file.
DISCORD_TOKEN = "Your Token"
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}


ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


str_music=[]
str_url=[]
song=[]
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""


@bot.command(name='Play', help='To play song')
async def Play(ctx, url):

    try:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    except:
        pass

    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_client = ctx.message.guild.voice_client
        song.append(url)

        x = 0
        while x < 3000:
            if voice_client.is_playing():
                await asyncio.sleep(2.3548)
                x = x + 1
            else:
                break

        async with ctx.typing():
            url1 = song.pop(0)
            print(url1)
            ydl_opts = {'format': 'bestaudio'}  # 這行開始不用下載
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url1, download=False)
                URL = info['formats'][0]['url']
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                                      'options': '-vn'}
            voice_channel.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))


    except:
        print("The bot is not connected to a voice channel.")


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
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
