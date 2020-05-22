class Player:
    def __init__(self, userID, firstScore = 0):
        self.userID = userID
        self.points = 0
        self.totalScore = firstScore
        self.mapsPlayed = 1
        self.Team = 0