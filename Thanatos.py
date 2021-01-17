import Cogs.osu.OsuApiAccessor as api
from collections import OrderedDict
from discord.ext import tasks, commands
from itertools import chain
import re

api.setup()
bot = commands.Bot(command_prefix='.')
credentials=open("credentials.txt", "r")    #file containing the discord authentication token

@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))




#.embed <title> : <body>
@bot.command()
async def embed(context, *, message):
    parsedMsg = message.split(':', 1)
    embed=discord.Embed(color=0xff80c0, description=parsedMsg[1], title = parsedMsg[0])



bot.run(credentials.read())
bot.add_cog(Osu(bot))