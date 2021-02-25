import discord
from discord.ext import tasks, commands
import Cogs.vndb.VndbApiAccessor as api
from Cogs.vndb.VisualNovel import VisualNovel as vn
import json

class VndbMain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        api.login()
        testVN()

def testVN():
    rawresponse = api.requestVnData(67)
    responsejson = json.loads(rawresponse)
    print("what if it dies")
    firstlistitem = responsejson["items"][0]
    testvn = vn(firstlistitem)
    print(testvn.title)