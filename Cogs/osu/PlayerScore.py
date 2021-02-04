import Cogs.osu.Team as Team

class PlayerScore:

    def __init__(self, playerID, score, team, passed, mod):
        self.playerID = playerID
        self.score = score
        self.team = team
        self.passed = passed
        self.mod = mod

