import Cogs.osu.PlayerScore
import Cogs.osu.Team
import Cogs.osu.Mode

class MatchMap:

    def __init__(self, mapID, mod, teamType):
        self.mapID = mapID
        self.blueScore=0
        self.redScore=0
        self.mod = mod
        self.teamType = teamType
        self.scores=dict()
        