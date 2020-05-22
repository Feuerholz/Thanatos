import osuApiAccessor as api
import Match
import MatchMap
import PlayerScore
import Player
from collections import OrderedDict



async def processMatch(matchID, ezMult = 1.0, failedScoresCount = True):
    matchjson = await api.getMatch(matchID)
    match = Match.Match(matchID, matchjson["match"]["name"])
    for game in matchjson["games"]:
        match.maps[game["beatmap_id"]]=MatchMap.MatchMap(game["beatmap_id"], int(game["mods"]), int(game["team_type"]))

        for score in game["scores"]:
            if(int(score["score"])>0):
                mod=0
                if(score["enabled_mods"]!=None):
                    mod = int(score["enabled_mods"])
                match.maps[game["beatmap_id"]].scores[score["user_id"]]=PlayerScore.PlayerScore(score["user_id"], int(score["score"]), int(score["team"]), bool(score["pass"]), mod)
                if(score["user_id"] not in match.players):
                    match.players[score["user_id"]]=Player.Player(score["user_id"], int(score["score"]))
                else:
                    match.players[score["user_id"]].mapsPlayed+=1
                    match.players[score["user_id"]].totalScore+=int(score["score"])

    for id, map in match.maps.items():
        if(map.teamType==2):
            match.teamType=2
            for id, score in map.scores.items():
                if(failedScoresCount or score.passed):
                    if(score.team==1):
                        if(score.mod & 2==2):
                            map.blueScore+=score.score*ezMult
                        else:
                            map.blueScore+=score.score
                    else:
                        if(score.mod & 2==2):
                            map.redScore+=score.score*ezMult
                        else:
                            map.redScore+=score.score


    return match

# calculates the match result for either a team vs or 1v1 match on a given mappool
def calculateMatchResult(match, pool):
    for id, map in match.maps.items():
        if(map.mapID in pool):
            if(match.teamType==2):
                if(map.redScore>map.blueScore):
                    match.redScore+=1
                elif(map.blueScore>map.redScore):
                    match.blueScore+=1
            elif(match.teamType==0):
                max=-1
                winid=-1
                for uid, score in map.scores.items():
                    if (score.score>max):
                        max=score.score
                        winid=int(score.playerID)
                if(winid>0):
                    match.players[winid].score+=1
                    
