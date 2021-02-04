import discord
import Cogs.osu.MatchProcessor as MatchProcessor
import Cogs.osu.MatchRating as MatchRating
import Cogs.osu.Match as Match
import Cogs.osu.Team as Team
import Cogs.osu.OsuApiAccessor as api
import Cogs.osu.TopScoreCalculator as tops
from collections import OrderedDict
from discord.ext import tasks, commands
from itertools import chain
import re


class OsuMain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    #.match <matchID>
    #   doesn't really do anything useful rn
    @commands.command()
    async def match(context, *, message):
        messageArr = message.split(' ')
        matchID = messageArr[0].split('/')[-1]
        match = await MatchProcessor.processMatch(matchid)



    @commands.command()
    async def test(self, ctx, *, arg):
        await ctx.send(arg)
    #.rating <matchID> <params>
    #params:
    #   -ez <number> to specify a multiplier for EZ mod (default: 1)
    #   -f to count failed scores as 0 points
    #   -w <integer> to specify number of warmups (default: 2)
    #   -b <number> to specify the bonus rating per played map (default: 0.1)
    @commands.command()
    async def rating(self, context, *, message):
        msg = message.split(' ')
        for m in msg:
            m = m.lower()
        matchID = msg[0].split('/')[-1]
        ezmult=1.0
        failsCount=True
        warmups=2
        playBonus = 0.1

        try:
            i = msg.index("-ez")
            ezmult=float(msg[i+1])
        except ValueError:
            pass
        try:
            i = msg.index("-f")
            failsCount=False
        except ValueError:
            pass
        try:
            i = msg.index("-w")
            warmups=int(msg[i+1])
        except ValueError:
            pass
        try:
            i = msg.index("-b")
            playBonus = float(msg[i+1])
        except ValueError:
            pass
        match = await MatchProcessor.processMatch(matchID, ezmult, failsCount)
        ratings = MatchRating.calculateMatchRatings(match, warmups, failsCount, playBonus)
        embed=discord.Embed(title=match.name, color=0x707070)
        i=1
        temp=[]

        for id, player in ratings.items():
            temp.append(player)
        players=sorted(temp, key=self.getRating, reverse=True)

        if(match.teamType==0):
            for player in players:
                print(player.userID)
                playerjson = await api.getUser(player.userID)
                playername = playerjson["username"]
                #every third field should be an empty field because it looks cluttered with 3 inline fields
                if(i%3==0):
                    embed.add_field(name='\u200b', value='\u200b', inline=True)
                    embed.add_field(name=playername, value=str(player.rating)[:4], inline=True)
                    i+=1
                else:
                    embed.add_field(name=playername, value=str(player.rating)[:4], inline=True)
                i+=1
            #add trailing empty field if number of players would leave 2 fields in the last line
            if(i%3==0):
                embed.add_field(name='\u200b', value='\u200b', inline=True)

        elif(match.teamType==2):
            teamnames=re.findall("\((.*?)\)", match.name)
            embed.add_field(name=teamnames[1], value='\u200b', inline=True)
            embed.add_field(name=teamnames[0], value='\u200b', inline=True)
            embed.add_field(name='\u200b', value='\u200b', inline=True)
            blueplayers=[]
            redplayers=[]
            for player in players:
                if(player.team==1):
                    blueplayers.append(player)
                elif(player.team==2):
                    redplayers.append(player)

            i=0

            #alternately add blue and red player embeds followed by an empty one
            while (i<(len(blueplayers))):
                print(blueplayers[i].userID)
                playerjson = await api.getUser(blueplayers[i].userID)
                playername = playerjson["username"]
                embed.add_field(name=playername, value=str(blueplayers[i].rating)[:4], inline=True)
                if(i<len(redplayers)):
                    print(redplayers[i].userID)
                    playerjson = await api.getUser(redplayers[i].userID)
                    playername = playerjson["username"]
                    embed.add_field(name=playername, value=str(redplayers[i].rating)[:4], inline=True)
                else:
                    embed.add_field(name='\u200b', value='\u200b', inline=True)
                embed.add_field(name='\u200b', value='\u200b', inline=True)

                i+=1
            #if there are more red players than blue players, add empty embeds for blue and the player embeds for red
            while (i<(len(redplayers))):
                embed.add_field(name='\u200b', value='\u200b', inline=True)
                print(redplayers[i].userID)
                playerjson = await api.getUser(redplayers[i].userID)
                playername = playerjson["username"]
                embed.add_field(name=playername, value=str(redplayers[i].rating)[:4], inline=True)
                i+=1
            embed.add_field(name='\u200b', value='\u200b', inline=True)

        await context.send(embed=embed)


    #.playercompare <matchID> <playername> <matchID> <playername>
    #   compares scores on maps played in both matches by blue/red team as specified
    #   -ez <number> to specify a multiplier for EZ mod (default: 1)
    #   -f to count failed scores as 0 points
    @commands.command()
    async def playercompare(self, context, *, message):
        msg = message.split(' ')
        for m in msg:
            m = m.lower()
        matchID1 = msg[0].split('/')[-1]
        matchID2 = msg[2].split('/')[-1]
        EZmult=1.0
        failsCount=True
        try:
            i = msg.index("-ez")
            ezmult=float(msg[i+1])
        except ValueError:
            pass
        try:
            i = msg.index("-f")
            failsCount=False
        except ValueError:
            pass

        match1=await MatchProcessor.processMatch(matchID1, EZmult, failsCount)
        match2=await MatchProcessor.processMatch(matchID2, EZmult, failsCount)

        player1ID = (await api.getUserByName(msg[1]))["user_id"]
        player2ID = (await api.getUserByName(msg[3]))["user_id"]

        if(matchID1==matchID2):
            maps = self.findSameMaps(match1, None, player1ID, player2ID)
        else:
            maps = self.findSameMaps(match1, match2, player1ID, player2ID)

        embed=discord.Embed(title="Map score comparison between " + msg[1] + " and " + msg[3], color=0x707070)
        for map in maps:
            json = await api.getMap(map)
            mapname = json[0]["artist"] + " - " + json[0]["title"] + " [" + json[0]["version"] +"]"
            formattedResults=""
            formattedResults+=str(match1.maps[map].scores[player1ID].score) + " | "
            formattedResults+=str(match2.maps[map].scores[player2ID].score)
            embed.add_field(name=mapname, value=formattedResults, inline=False)

        await context.send(embed=embed)


    #.matchcompare <matchID> <b/r><1/2> <matchID> <b/r><1/2> <params>
    #   compares scores on maps played in both matches by blue/red team as specified. 
    #   The number after b or r is needed to get the correct team name from the mp lobby, 1 gets the first name, 2 the second.
    #   -ez <number> to specify a multiplier for EZ mod (default: 1)
    #   -f to count failed scores as 0 points
    @commands.command()
    async def matchcompare(self, context, *, message):
        msg = message.split(' ')
        matchID1 = msg[0].split('/')[-1]
        matchID2 = msg[2].split('/')[-1]
        EZmult=1.0
        failsCount=True
        try:
            i = msg.index("-ez")
            ezmult=float(msg[i+1])
        except ValueError:
            pass
        try:
            i = msg.index("-f")
            failsCount=False
        except ValueError:
            pass
        match1=await MatchProcessor.processMatch(matchID1, EZmult, failsCount)
        match2=await MatchProcessor.processMatch(matchID2, EZmult, failsCount)
        maps = self.findSameMaps(match1, match2)
        if(msg[1]=='b1'):
            team1=1
            team1name = re.findall("\((.*?)\)", match1.name)[0]
        elif(msg[1]=='b2'):
            team1=1
            team1name = re.findall("\((.*?)\)", match1.name)[1]
        elif(msg[1]=='r1'):
            team1=2
            team1name = re.findall("\((.*?)\)", match1.name)[0]
        elif(msg[1]=='r2'):
            team1=2
            team1name = re.findall("\((.*?)\)", match1.name)[1]
        if(msg[3]=='b1'):
            team2=1
            team2name = re.findall("\((.*?)\)", match2.name)[0]
        elif(msg[3]=='b2'):
            team2=1
            team2name = re.findall("\((.*?)\)", match2.name)[1]
        elif(msg[3]=='r1'):
            team2=2
            team2name = re.findall("\((.*?)\)", match2.name)[0]
        elif(msg[3]=='r2'):
            team2=2
            team2name = re.findall("\((.*?)\)", match2.name)[1]
        embed=discord.Embed(title="Map score comparison between " + team1name + " and " + team2name, color=0x707070)

        for map in maps:
            json = await api.getMap(map)
            mapname = json[0]["artist"] + " - " + json[0]["title"] + " [" + json[0]["version"] +"]"
            formattedResults=""
            if(team1 == 1):
                formattedResults+=str(match1.maps[map].blueScore) + " | "
            if(team1 == 2):
                formattedResults+=str(match1.maps[map].redScore) + " | "
            if(team2 == 1):
                formattedResults+=str(match2.maps[map].blueScore)
            if(team2 == 2):
                formattedResults+=str(match2.maps[map].redScore)
            embed.add_field(name=mapname, value=formattedResults, inline=False)

        await context.send(embed=embed)

    #.derank <playername> <map rank in tops> <new pp of overwritten play>
    #   calculates new pp total if a specified play was overwritten with a new pp value
    #   duplicates the #100 play for calculation purposes if the new pp values is lower than the players' current #100
    #   currently bugged and idk why
    @commands.command()
    async def derank(self, context, *, message):
        msg = message.split()
        player = msg[0]
        play = int(msg[1])
        newpp = float(msg[2])
        userpp = await tops.calculatePP(player, play, newpp)
        embed = discord.Embed(title="PP difference for " + str(player) + " if the #" + str(play) + " top play was overwritten with a " + str(newpp) + "pp score", color=0x707070)
        embed.add_field(name="old PP", value='%.2f'%(userpp[0]))
        embed.add_field(name="new PP", value='%.2f'%(userpp[1]))
        embed.add_field(name="PP difference", value='%.2f'%(userpp[0]-userpp[1]))
    
        await context.send(embed=embed)


    #.newtop <playername> <pp amount>
    #   calcualates new pp total if the player got a play with the specified amount of pp
    #   currently bugged and idk why
    @commands.command()
    async def newtop(self, context, *, message):
        msg = message.split()
        player = msg[0]
        newpp = flot(msg[1])
        userpp = await tops.calculatePP(player, 100, newpp)
        embed = discord.Embed(title="PP difference for " + str(player) + " if they got a " + str(newpp) + "pp score", color=0x707070)
        embed.add_field(name="old PP", value='%.2f'%(userpp[0]))
        embed.add_field(name="new PP", value='%.2f'%(userpp[1]))
        embed.add_field(name="PP difference", value='%.2f'%(userpp[0]-userpp[1]))
    
        await context.send(embed=embed)

    def getRating(self, player):
        return player.rating

    # find overlapping maps in two given matches and return the list of map IDs
    def findSameMaps(self, match1, match2 = None, playerID1 = None, playerID2 = None):
        returnList = []
        if(match2 == None):
            for id, map in match1.maps.items():
                if (playerID1 in map.scores.keys() and playerID2 in map.scores.keys()):
                    returnList.append(map.mapID)

        elif (playerID1 == None):
            for id, map1 in match1.maps.items():
                for id, map2 in match2.maps.items():
                    if (map1.mapID == map2.mapID):
                        returnList.append(map1.mapID)
                        break
        else:
            for id, map1 in match1.maps.items():
                for id, map2 in match2.maps.items():
                    if (map1.mapID == map2.mapID):
                        if (playerID1 in map1.scores.keys() and playerID2 in map2.scores.keys()):
                            returnList.append(map1.mapID)
                            break
        return returnList
