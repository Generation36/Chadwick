import discord
from discord.ext import commands
import logging

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
General commands:
/help - displays all the available commands
/p, /play <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current song if it was paused
/q, /queue - displays the current music queue
/skip - skips the current song being played
/clear - Stops the music and clears the queue
/leave - Disconnected the bot from the voice channel
/pause - pauses the current song being played or resumes if already paused
/resume - resumes playing the current song
```
"""
        self.text_channel_text = []
    
    # start up command
    @commands.Cog.listener()
    async def on_ready(self):
        logging.debug("Chadwick is live and waiting for commands...")
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.name == 'bot':
                    await channel.send("Chadwick is live and waiting for commands...")
    
    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        logging.debug(f"Recognised that a member called {ctx.name} joined")
        try: 
            guild = ctx.guild
            if guild.system_channel is not None:
                to_send = f'Welcome {ctx.mention} to the Shit Show'
                await guild.system_channel.send(to_send)
        except:
            print("Couldn't message " + ctx.name) 

    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)