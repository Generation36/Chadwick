import discord, os, random, youtube_dl, asyncio
from discord.ext import commands

# possibly needed for youtube links
intents = discord.Intents().default()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)


# Greet new member when they join server
# @bot.event
# async def new_member_joined_server(ctx, new_member):
    # await ctx.channel.send("0.{new_member} has joined the server!".format(new_member))

# Play Youtube Links
youtube_dl.utils.bug_reports_message = 'lambda'

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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options' : '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, original, *, data, volume=0.1):
        super().__init__(original, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        
        return filename

# Hello Function
@bot.command(brief='Chadwick will greet you')
async def hello(ctx):
    n = random.randint(0,1000)
    if(n%2 == 0):
        await ctx.channel.send('Hello!')
    else:
        await ctx.channel.send('Oi Cunt!')

# Join Channel
@bot.command(name='join', brief='Tells bot to join the channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return 
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

# Leave Channel
@bot.command(name='leave', brief='Tells the bot to leave the channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel")

### Make sure to give the bot proper permissions/roles in the server so it can the desired voice channel

# Play Video
@bot.command(name='play', brief='Plays a desired youtube video')
async def play(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable='ffmpeg', source=filename))
        await ctx.send("**Now playing:**{}".format(filename))
    except:
        await ctx.send("Chadwick is not connected to a voice channel.")

# Pause Video
@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("Chadwick is not playing anything at the moment.")
    
# Resume Video
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("Chadwick was not playing anything before this. Use play_song command")

# Stop Video
@bot.command(name='stop', brief='Stops the currently playing video')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("Chadwick is currently not playing anything")

# Display all users within server
@bot.command(name='users', brief='Displays all users Chadwick is aware about in the current server/guild')
async def users(ctx):
    server = ctx.message.guild
    message = "Chadwick can see:\n"
    for user in server.members:
        message = message + str(user) + '\n'
    await ctx.send(message)
    
# Greet New Member upon joining
@bot.event
async def on_member_join(member):
    print("Recognised that a member called " + member.name + " joined")
    try: 
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to the Shit Show'
            await guild.system_channel.send(to_send)
    except:
        print("Couldn't message " + member.name)

# Assign a role to a user
# @bot.command(name="new_role", brief="Give a user a new role"):
#     async def new_role(member, role):
#         if 
# Startup Function
@bot.event
async def on_ready():
    print("Chadwick bot is going live..")

from dotenv import load_dotenv
load_dotenv()

bot.run(os.getenv('TOKEN'))