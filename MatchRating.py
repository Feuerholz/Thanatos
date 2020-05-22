import Match
import Player
import MatchMap
from collections import OrderedDict


#newrating = oldrating+K(achievedpoints-expectedpoints)

class EloPlayer:
    def __init__(self, userID):
        self.expectedScore = 0
        self.actualScore = 0
        self.userID = userID
        self.mapsPlayed = 0
        self.rating = 1.0
        self.team = 0

    def __iter__(self):
        return EloPlayerIterator(self)

def calculateMatchRatings(match, warmups = 2, failedScoresCount = True, playBonus = 0.1):
    players = dict()
    returnDict = dict()
    nPlayers = 2
    nMaps = 0 - warmups
    for id, player in match.players.items():
        players[player.userID] = EloPlayer(player.userID)
    for id, map in match.maps.items():
        totalscore = 0
        if(nMaps<0):
            nMaps+=1
        else:
            nMaps+=1
            for uid, score in map.scores.items():
                totalscore+=score.score
                if(players[uid].team==0):
                    players[uid].team = score.team

            expectedscore = 1/len(map.scores)
            if(len(map.scores)>nPlayers):
                nPlayers = len(map.scores)
            for uid, score in map.scores.items():
                players[score.playerID].expectedScore+=expectedscore
                players[uid].mapsPlayed+=1
                if(failedScoresCount or score.passed):
                    players[score.playerID].actualScore+=score.score/totalscore
    for id, player in players.items():
        players[id].rating = (1.0+nPlayers*0.4*(player.actualScore-player.expectedScore)+player.mapsPlayed*playBonus)/max((0.25*pow(nMaps, 0.9)*playBonus*10), 1)
            
    return players