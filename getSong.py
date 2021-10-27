import search

from song import Song
from player import Player
from globals import defaultSong
from globals import players

async def getSong(message, thisGuildsPlayer):

    if message.author.voice == None:
        return await message.channel.send("*You have to be in a voice channel to do that command*")

    if thisGuildsPlayer != None and thisGuildsPlayer.voiceClient.is_paused() and len(message.content.split(" ")) < 2:
        await thisGuildsPlayer.unpause()
        await message.add_reaction("👍")
        return

    messageText = ""

    if len(message.content.split(" ")) < 2:
        if defaultSong == "":
            return await message.channel.send(f"*You have to put what you want to play after the command!* Like `{config['prefix']}play fly me to the moon`")
        messageText = defaultSong
    else:
        messageText = " ".join(message.content.split(" ")[1:])

    sentMessage = await message.channel.send(f"**Searching** `{messageText}`...")

    song = search.OnComputer(messageText)
    if song == None:
        print("No luck on computer")
        song = await search.OnYoutube(messageText, sentMessage)
        if song == None: return

    if thisGuildsPlayer == None:
        thisGuildsPlayer = Player(message.guild, [song], message.channel)
        players.append(thisGuildsPlayer)
        await thisGuildsPlayer.joinAndPlay(message, sentMessage)
    else:
        thisGuildsPlayer.queue.append(song)
        await sentMessage.edit(content=f"**Added** `{song.name}` to queue")
