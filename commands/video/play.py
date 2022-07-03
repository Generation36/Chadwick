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