import Cogs.osu
import Cogs.osu.OsuApiAccessor as api
from Cogs.osu.OsuMain import OsuMain
from Cogs.vndb.VndbMain import VndbMain
import Cogs.vndb.VndbApiAccessor
from collections import OrderedDict
from discord.ext import tasks, commands
from itertools import chain
import re
import logging

bot = commands.Bot(command_prefix='.')
credentials=open("credentials.txt", "r")    #file containing the discord authentication token


@bot.event
async def on_ready():
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)
    outputFileHandler = logging.FileHandler("Thanatos.log")
    consoleHandler = logging.StreamHandler(sys.stdout)

    logging.info('logged in as {0.user}'.format(bot))
    bot.add_cog(Cogs.osu.OsuMain.OsuMain(bot))
    logging.info("successfully loaded osu! Cog")
    bot.add_cog(Cogs.vndb.VndbMain.VndbMain(bot))
    logging.info("successfully loaded VNDB Cog")




#.embed <title> : <body>
@bot.command()
async def embed(context, *, message):
    parsedMsg = message.split(':', 1)
    embed=discord.Embed(color=0xff80c0, description=parsedMsg[1], title = parsedMsg[0])



bot.run(credentials.read())