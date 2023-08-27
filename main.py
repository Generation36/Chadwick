import discord
from discord.ext import commands
import os

from help_cog import help_cog
from music_cog import music_cog


bot = commands.Bot(command_prefix='/')
bot.remove_command("help")

# @bot.event
# async def on_member_join(ctx):
#     print("Recognised that a member called " + ctx.name + " joined")
#     try: 
#         guild = ctx.guild
#         if guild.system_channel is not None:
#             to_send = f'Welcome {ctx.mention} to the Shit Show'
#             await guild.system_channel.send(to_send)
#     except:
#         print("Couldn't message " + ctx.name)

# Join Channel
@bot.command(name='join', brief='Tells bot to join the channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return 
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.event
async def on_ready():
    print("Chadwick bot is going live..")

bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))

from dotenv import load_dotenv
load_dotenv()

bot.run(os.getenv('TOKEN'))