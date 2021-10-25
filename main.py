import discord
import json
import os
import asyncio
import time

from globals import songList

from pytube import YouTube
from pytube import Search

config = json.load(open("config.json"))

client = discord.Client()

players = []

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
    songList.append(Song(i["filePath"], i["songId"], i["name"], i["thumbnail"], i["fileSize"], i["dateAdded"]))

async def getSong(message, thisGuildsPlayer):
    if len(message.content) < 2:
        return await message.channel.send(f"You have to put what you want to play after the command! Like `{config['prefix']}play fly me to the moon`")

    if (message.author.voice == None):
        return await message.channel.send("*You have to be in a voice channel to do that command*")

    messageText = " ".join(message.content.split(" ")[1:])

    song = search.OnComputer(messageText)
    if song == None:
        print("No luck on computer")
        song = await search.OnYoutube(messageText)
        if song == None: return

    if thisGuildsPlayer == None:
        thisGuildsPlayer = Player(message.guild, [song], message.channel)
        players.append(thisGuildsPlayer)
        await thisGuildsPlayer.joinAndPlay(message)
    else:
        thisGuildsPlayer.queue.append(song)

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

    if args[0] == "play" or args[0] == "p":
        await getSong(message, thisGuildsPlayer)
    else:
        await message.channel.send(f"Not a command {args}")
    
client.run(config["token"])