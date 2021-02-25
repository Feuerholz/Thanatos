import discord
from discord.ext import tasks, commands

class VndbMain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
