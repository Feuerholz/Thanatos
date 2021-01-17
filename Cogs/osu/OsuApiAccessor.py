import requests as req
import Cogs.osu.Mode

OSU_URL = 'http://osu.ppy.sh/api/'
def setup():
	with open ("osuapikey.txt", "r") as apifile:
		global API_KEY
		API_KEY= apifile.read().replace('\n', '')

#osu! API doc can be found at https://github.com/ppy/osu-api/wiki

async def getRecentPlays(user, numberOfPlays=1, mode=0):
	response = req.get(OSU_URL + 'get_user_recent', params = {'k':API_KEY, 'u':user, 'm':mode, 'limit':numberOfPlays, 'type':'string'})
	return response.json()

async def getMatch(matchID):
	response = req.get(OSU_URL + 'get_match', params = {'k':API_KEY, 'mp':matchID})
	return response.json()

async def getMap(mapID):
	response = req.get(OSU_URL + 'get_beatmaps', params = {'k':API_KEY, 'b':mapID})
	return response.json()

async def getUser(userID):
	response = req.get(OSU_URL + 'get_user', params = {'k':API_KEY, 'u':userID, 'type':"id"})
	return response.json()[0]

async def getUserByName(username):
	response = req.get(OSU_URL + 'get_user', params = {'k':API_KEY, 'u':username, 'type':"string"})
	return response.json()[0]

async def getUserTops(username):
	response = req.get(OSU_URL + 'get_user_best', params = {'k':API_KEY, 'limit':100, 'u':username, 'type':"string"})
	return response.json()