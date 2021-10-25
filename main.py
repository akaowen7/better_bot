import discord
import json
import os
import asyncio
import time

from globals import songList
from globals import players

from pytube import YouTube
from pytube import Search

config = json.load(open("config.json"))

client = discord.Client()

from song import Song
from player import Player
import search

if not os.path.isfile("./song_list.json"):
    data = {}
    data["songs"] = []
    with open('song_list.json', 'w') as outfile:
        json.dump(data, outfile)

jsonSongList = json.load(open("song_list.json"))["songs"]

for i in jsonSongList:
    songList.append(Song(i["filePath"], i["songId"], i["name"], i["thumbnail"], i["fileSize"], i["dateAdded"], i["length"]))

async def getSong(message, thisGuildsPlayer):

    if message.author.voice == None:
        return await message.channel.send("*You have to be in a voice channel to do that command*")

    if thisGuildsPlayer != None and thisGuildsPlayer.voiceClient.is_paused() and len(message.content.split(" ")) < 2:
        await thisGuildsPlayer.unpause(message)
        return

    if len(message.content.split(" ")) < 2:
        return await message.channel.send(f"You have to put what you want to play after the command! Like `{config['prefix']}play fly me to the moon`")

    sentMessage = await message.channel.send(f"Searching...")

    messageText = " ".join(message.content.split(" ")[1:])

    song = search.OnComputer(messageText)
    if song == None:
        print("No luck on computer")
        song = await search.OnYoutube(messageText, sentMessage)
        if song == None: return

    await sentMessage.delete()

    if thisGuildsPlayer == None:
        thisGuildsPlayer = Player(message.guild, [song], message.channel)
        players.append(thisGuildsPlayer)
        await thisGuildsPlayer.joinAndPlay(message, sentMessage)
    else:
        thisGuildsPlayer.queue.append(song)
        await message.add_reaction("👍")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot: return
    if not message.content.startswith(config["prefix"]): return
    
    args = message.content.replace(config["prefix"], "").split(" ")

    thisGuildsPlayer = None
    for i in players:
        if i.guild == message.guild:
            thisGuildsPlayer = i
            break

    commands = {
        "play": 1,
        "p": 1,
        "skip": 2,
        "pause": 3,
        "queue": 4
    }       
    command = commands[args[0].lower()]

    if command == 1:
        await getSong(message, thisGuildsPlayer)
    elif command == 2:
        await thisGuildsPlayer.skip(message)
    elif command == 3:
        await thisGuildsPlayer.pause(message)
    else:
        await message.channel.send(f"Not a command {args}")
    
client.run(config["token"])