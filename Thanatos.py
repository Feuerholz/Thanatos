import discord

CMD_PREFIX = '.'

client = discord.Client()
credentials=open("credentials.txt", "r")    #file containing the discord authentication token

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(CMD_PREFIX + 'embed'):
        msgToParse = message.content
        msgToParse = msgToParse.replace(CMD_PREFIX + 'embed', '')
        parsedMsg = msgToParse.split(':', 1)

        embed = discord.Embed()
        embed=discord.Embed(color=0xff80c0, description=parsedMsg[1], title = parsedMsg[0])
        await message.channel.send(embed=embed)
        await message.delete()

    

client.run(credentials.read())
