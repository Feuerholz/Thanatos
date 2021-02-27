import discord
from discord.ext import tasks, commands
import Cogs.vndb.VndbApiAccessor as api
from Cogs.vndb.VisualNovel import VisualNovel as vn
import json
import logging

class VndbMain(commands.Cog):
    def __init__(self, bot):
        try:
            self.bot = bot
            self._last_member = None
        except Exception as e:
            logging.error("Error intitializing VNDB Cog: {0}".format(e))
        try:
          api.login()
        except Exception as e:
            logging.error("Error logging into VNDB API: {0}".format(e))

    #.vn [name|id]
    #   looks up a vn either by name or id in vndb (assumes id if positive integer, name otherwise)
    @commands.command()
    async def vn(self, context, *, message):
        try:
            msg = message.split(' ')
            #If it's a positive integer, look up vn by id
            if len(msg)==1 and msg[0].isnumeric():         
                rawresponse = api.requestVnData(id = message)
            else:
                rawresponse = api.requestVnData(title = message)
            responsedict = json.loads(rawresponse)
            logging.info("Query complete, number of results: {0}".format(len(responsedict["items"])))
            firstresult = responsedict["items"][0]
            vnresult = vn(firstresult)

            #making discord embeds is a pain
            embed=discord.Embed(title=vnresult.title, url="https://vndb.org/v{0}".format(vnresult.id), color=0x707070)

            #set embed author to the VNs original title
            if vnresult.original is not None:
                embed.set_author(name=vnresult.original, url="https://vndb.org/v{0}".format(vnresult.id))

            #only show thumbnail if it's not likely NSFW (maybe add a per server toggle/rating threshold for that at some point)
            if vnresult.image is not None and vnresult.image_flagging is not None and vnresult.image_flagging["votecount"]>5 and vnresult.image_flagging["sexual_avg"]<1.5 and vnresult.image_flagging["violence_avg"]<1.9:
                embed.set_thumbnail(url=vnresult.image)

            #Add a field showing the VNs length
            embed.add_field(name="Length", value=vnresult.lengthAsString())

            #Add a field showing the VNs rating on VNDB
            embed.add_field(name="Rating", value="{0} in {1} votes".format(vnresult.rating, vnresult.votecount))

            #Add a field showing the VNs languages, with original language in bold
            embed.add_field(name="Languages", value=vnresult.formattedLanguages())

            #Add a field showing the VNs release date
            embed.add_field(name="Initial release date", value=vnresult.released)

            #Add a field showing the platforms the VN was released for
            embed.add_field(name="Platforms", value=vnresult.formattedPlatforms())

            #Add empty field bc discord sucks
            embed.add_field(name='\u200b', value='\u200b')

            await context.send(embed=embed)
            logging.info("Embed for VN {0} sent successfully".format(vnresult.id))

        except Exception as e:
            logging.error("error finding vn, error: {0}".format(e))


