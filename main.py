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
        await thisGuildsPlayer.unpause()
        await message.add_reaction("👍")
        return

    if len(message.content.split(" ")) < 2:
        return await message.channel.send(f"*You have to put what you want to play after the command!* Like `{config['prefix']}play fly me to the moon`")

    sentMessage = await message.channel.send(f"**Searching** `{' '.join(message.content.split(' ')[1:])}`...")

    messageText = " ".join(message.content.split(" ")[1:])

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
        "help": 0,
        "h": 0,
        "commands": 0,
        "play": 1,
        "p": 1,
        "skip": 2,
        "pause": 3,
        "h": 3,
        "queue": 4,
        "q": 4,
        "leave": 5,
        "fuckoff": 5,
        "quit": 5
    }       
    command = commands[args[0].lower()]

    if command == 0:
        emb = discord.Embed(title = "Help", description = "", color=0x1CB8B1)
        emb.set_author(name=message.guild.name, icon_url="https://cdn.discordapp.com/avatars/654147464357609519/03a12bea6dc1d7600fb41c0317445f4a.png?size=4096")
        emb.add_field(name=f"{config['prefix']}play <song>", value=f"Plays the song off youtube, can accept a title or a link.\nAlisis: `{config['prefix']}p`", inline=False)
        emb.add_field(name=f"{config['prefix']}skip", value=f"Skips to the next song in queue. If there is none, tells the bot to leave\nAlisis: see what happens when you send `{config['prefix']}s`", inline=False)
        emb.add_field(name=f"{config['prefix']}pause", value=f"Pauses the current song\nAlisis: `{config['prefix']}h`", inline=False)
        emb.add_field(name=f"{config['prefix']}queue", value=f"Displays the queue of songs to be played\nAlisis: `{config['prefix']}q`", inline=False)
        emb.add_field(name=f"{config['prefix']}leave", value=f"Makes the bot leave the chat, current queue is lost\nAlisis: `{config['prefix']}fuckoff` `{config['prefix']}quit`", inline=False)
        await message.channel.send(embed=emb)

    if thisGuildsPlayer == None and command > 1:
        await message.channel.send(f"**Nothing is playing right now!** Send `{config['prefix']}play` and a song to get started")

    if command == 1:
        await getSong(message, thisGuildsPlayer)
        return
    
    if thisGuildsPlayer.voiceClient.channel != message.author.voice.channel:
        await message.channel.send(f"*You need to be in the audio channel where I am to do that*")

    if command == 2:
        thisGuildsPlayer.skip()
        await message.add_reaction("👍")
    elif command == 3:
        thisGuildsPlayer.pause()
        await message.channel.send("**Paused**, send the `play` command to resume")
    elif command == 4:
        await thisGuildsPlayer.sendQueue(message)
    elif command == 5:
        thisGuildsPlayer.fuckoff()
    else:
        await message.channel.send(f"Not a command {args}")

@client.event
async def on_reaction_add(reaction, user):

    thisGuildsPlayer = None
    for i in players:
        if i.guild == reaction.message.guild:
            thisGuildsPlayer = i
            break

    if user.id == client.user.id:
        if reaction.emoji == "⏭️":
            thisGuildsPlayer.nowPlayingMessage = reaction.message
        else:
            return
    
    if user.bot: return

    if thisGuildsPlayer == None:
        return

    if reaction.message == thisGuildsPlayer.nowPlayingMessage:

        if reaction.emoji == "⏸" and not thisGuildsPlayer.voiceClient.is_paused():
            await reaction.message.clear_reactions()
            thisGuildsPlayer.pause()
            for i in ["▶️", "⏭️"]:
                await reaction.message.add_reaction(i)

        if reaction.emoji == "▶️" and thisGuildsPlayer.voiceClient.is_paused():
            await reaction.message.clear_reactions()
            thisGuildsPlayer.unpause()
            for i in ["⏸", "⏭️"]:
                await reaction.message.add_reaction(i)
        
        if reaction.emoji == "⏭️":
            thisGuildsPlayer.skip()

    
client.run(config["token"])