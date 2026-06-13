import discord
from discord.ext import commands
import yt_dlp

TOKEN = "MTUxNTA3NTk1Njc0ODk3NjI1OQ.GF1xgs.dH5RKKxauSZ6tv8SnoCH4EqGHS1hJJBwZ3ASVk"

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} is online!")

@client.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("❌ You are not in a voice channel!")
        return

    channel = ctx.author.voice.channel
    voice = ctx.voice_client

    if voice is None:
        await channel.connect()
    else:
        await voice.move_to(channel)

    await ctx.send("🎤 Joined voice channel!")

@client.command()
async def play(ctx, *, url):

    if ctx.author.voice is None:
        await ctx.send("❌ You must be in a voice channel!")
        return

    channel = ctx.author.voice.channel
    voice = ctx.voice_client

    if voice is None:
        voice = await channel.connect()
    elif not voice.is_connected():
        voice = await channel.connect()
    else:
        await voice.move_to(channel)

    ydl_opts = {'format': 'bestaudio', 'noplaylist': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']

    source = discord.FFmpegPCMAudio(audio_url)
    voice.play(source)

    await ctx.send(f"🎵 Now Playing: {info['title']}")

@client.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left voice channel")

client.run("MTUxNTA3NTk1Njc0ODk3NjI1OQ.GF1xgs.dH5RKKxauSZ6tv8SnoCH4EqGHS1hJJBwZ3ASVk")
