import osuApiAccessor as api
import discord

#returns a formatted text response for the discord server for a request about any users' most recent play(s)
async def recent(user, numberOfPlays=1, mode=0):
	data = await api.getRecentPlays(user, numberOfPlays, mode)
	for play in data:
		bmID = play['beatmap_id']
		score = play['score']
		maxcombo = play['maxcombo']
		count50 = play['count50']
		count100 = play['count100']
		count300 = play['count300']
		countmiss = play['countmiss']
		mods = play['enabled_mods']
		timestamp = play['date']
		rank = play['rank']

	embed = discord.Embed()
	embed=discord.Embed(description="<:zelda_flask:570386788997267456> **727.27pp** (737.37 for FC) \n**69.69%** | **727**/737x\n 1234567 | [300/100/50/1]\n 7 minutes 27 seconds ago")
	embed.set_author(name="Artist - Title [Difficulty] +Mods [6.66★]", url="http://osu.ppy.sh/")
	embed.set_thumbnail(url="https://i.imgur.com/4U8IyE7.jpg")
	return embed


