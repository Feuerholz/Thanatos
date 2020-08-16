from collections import OrderedDict


class Match:
    def __init__(self, matchID, name):
        self.matchID = matchID
        self.redScore = 0
        self.blueScore = 0
        self.maps = OrderedDict()
        self.name = name
        self.players = dict()
        self.teamType = 0

    def __iter__(self):
        return MatchIterator(self)