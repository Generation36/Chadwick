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

bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))

from dotenv import load_dotenv
load_dotenv()

bot.run(os.getenv('TOKEN'))