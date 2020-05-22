import discord
import MatchProcessor
import MatchRating
import Match
import Team
import osuApiAccessor as api
from collections import OrderedDict
from discord.ext import tasks, commands
from itertools import chain
import re

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


#.match <matchID>
@bot.command()
async def match(context, *, message):
    messageArr = message.split(' ')
    matchID = messageArr[0].split('/')[-1]
    match = await MatchProcessor.processMatch(matchid)



@bot.command()
async def test(ctx, *, arg):
    await ctx.send(arg)
#.rating <matchID> <params>
#params:
#   -ez <number> to specify a multiplier for EZ mod (default: 1)
#   -f to count failed scores as 0 points
#   -w <number> to specify number of warmups (default: 2)
@bot.command()
async def rating(context, *, message):
    msg = message.split(' ')
    matchID = msg[0].split('/')[-1]
    ezmult=1.0
    failsCount=True
    warmups=2
    playBonus = 0.1
    for i in range(1, len(msg)):
        if (msg[i].lower() == "-ez"):
            ezmult=float(msg[i+1])
            i=i+1
        elif (msg[i].lower() == "-f"):
            failsCount=False
        elif (msg[i].lower() == "-w"):
            warmups=int(msg[i+1])
            i=i+1
        elif (msg[i].lower() == "-b"):
            playBonus = float(msg[i+1])
            i=i+1
    match = await MatchProcessor.processMatch(matchID, ezmult, failsCount)
    ratings = MatchRating.calculateMatchRatings(match, warmups, failsCount, playBonus)
    embed=discord.Embed(title=match.name, color=0x707070)
    i=1
    temp=[]

    for id, player in ratings.items():
        temp.append(player)
    players=sorted(temp, key=getRating, reverse=True)

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
@bot.command()
async def playercompare(context, *, message):
    msg = message.split(' ')
    matchID1 = msg[0].split('/')[-1]
    matchID2 = msg[2].split('/')[-1]
    EZmult=1.0
    failsCount=True
    #if (msg[4]=='-ez'):
     #   if(msg[5]!=None):
     #       EZmult=int(msg[5])
    match1=await MatchProcessor.processMatch(matchID1, EZmult, failsCount)
    match2=await MatchProcessor.processMatch(matchID2, EZmult, failsCount)

    player1ID = (await api.getUserByName(msg[1]))["user_id"]
    player2ID = (await api.getUserByName(msg[3]))["user_id"]

    if(matchID1==matchID2):
        maps = findSameMaps(match1, None, player1ID, player2ID)
    else:
        maps = findSameMaps(match1, match2, player1ID, player2ID)

    embed=discord.Embed(title="Map score comparison between " + msg[1] + " and " + msg[3], color=0x707070)
    for map in maps:
        json = await api.getMap(map)
        mapname = json[0]["artist"] + " - " + json[0]["title"] + " [" + json[0]["version"] +"]"
        formattedResults=""
        formattedResults+=str(match1.maps[map].scores[player1ID].score) + " | "
        formattedResults+=str(match2.maps[map].scores[player2ID].score)
        embed.add_field(name=mapname, value=formattedResults, inline=False)

    await context.send(embed=embed)


#.matchcompare <matchID> <b/r> <matchID> <b/r>
#   compares scores on maps played in both matches by blue/red team as specified
#   -ez <number> to specify a multiplier for EZ mod (default: 1)
#   -f to count failed scores as 0 points
@bot.command()
async def matchcompare(context, *, message):
    msg = message.split(' ')
    matchID1 = msg[0].split('/')[-1]
    matchID2 = msg[2].split('/')[-1]
    EZmult=1.0
    failsCount=True
    #if (msg[4]=='-ez'):
    #    if(msg[5]!=None):
    #        EZmult=int(msg[5])
    match1=await MatchProcessor.processMatch(matchID1, EZmult, failsCount)
    match2=await MatchProcessor.processMatch(matchID2, EZmult, failsCount)
    maps = findSameMaps(match1, match2)
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

def getRating(player):
    return player.rating

# find overlapping maps in two given matches and return the list of map IDs
def findSameMaps(match1, match2 = None, playerID1 = None, playerID2 = None):
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

bot.run(credentials.read())
