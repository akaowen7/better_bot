import discord
import json
import os

from globals import songList
from globals import players
from globals import commands

config = json.load(open("config.json"))

client = discord.Client()

from song import Song
from getSong import getSong

if not os.path.isfile("./song_list.json"):
    data = {}
    data["songs"] = []
    with open('song_list.json', 'w') as outfile:
        json.dump(data, outfile)

jsonSongList = json.load(open("song_list.json"))["songs"]

for i in jsonSongList:
    songList.append(Song(i["filePath"], i["songId"], i["name"], i["thumbnail"], i["fileSize"], i["dateAdded"], i["length"], i["neverDelete"]))

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

async def musicCommands(command, message):

    thisGuildsPlayer = None
    for i in players:
        if i.guild == message.guild:
            thisGuildsPlayer = i
            break

    if command == 0:
        emb = discord.Embed(title = "Help", description = "", color=0x1CB8B1)
        emb.set_author(name=message.guild.name, icon_url="https://cdn.discordapp.com/avatars/654147464357609519/03a12bea6dc1d7600fb41c0317445f4a.png?size=4096")
        emb.add_field(name=f"{config['prefix']}play <song>", value=f"Plays the song off youtube, can accept a title or a link.\nAlisis: `{config['prefix']}p`", inline=False)
        emb.add_field(name=f"{config['prefix']}skip", value=f"Skips to the next song in queue. If there is none, tells the bot to leave\nAlisis: see what happens when you send `{config['prefix']}s`", inline=False)
        emb.add_field(name=f"{config['prefix']}pause", value=f"Pauses the current song\nAlisis: `{config['prefix']}h`", inline=False)
        emb.add_field(name=f"{config['prefix']}queue", value=f"Displays the queue of songs to be played\nAlisis: `{config['prefix']}q`", inline=False)
        emb.add_field(name=f"{config['prefix']}leave", value=f"Makes the bot leave the chat, current queue is lost\nAlisis: `{config['prefix']}fuckoff` `{config['prefix']}quit`", inline=False)
        await message.channel.send(embed=emb)
        return

    if thisGuildsPlayer == None and command > 1:
        await message.channel.send(f"**Nothing is playing right now!** Send `{config['prefix']}play` and a song to get started")
        return

    if command == 1:
        await getSong(message, thisGuildsPlayer)
        return
    
    if message.author.voice == None or thisGuildsPlayer.voiceClient.channel != message.author.voice.channel:
        await message.channel.send(f"*You need to be in the voice channel where I am to do that*")
        return

    if command == 2:
        thisGuildsPlayer.skip()
        await message.add_reaction("👍")
    elif command == 3:
        await thisGuildsPlayer.pause()
        await message.channel.send("**Paused**, send the `play` command to resume")
    elif command == 4:
        await thisGuildsPlayer.sendQueue(message)
    elif command == 5:
        thisGuildsPlayer.fuckoff()

async def mcCommands(command, message):
    if command == 6:
        # await message.channel.send(f"Not a command {args}")
        pass

@client.event
async def on_message(message):
    if message.author.bot: return
    if not message.content.startswith(config["prefix"]): return
    
    args = message.content.replace(config["prefix"], "").split(" ")
   
    if args[0].lower() not in commands:
        await message.channel.send(f"Not a command {args}")
        return

    command = commands[args[0].lower()]

    if command <= 5:
        await musicCommands(command, message)
    else:
        mcCommands(command, message)


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
            await thisGuildsPlayer.pause()

        if reaction.emoji == "▶️" and thisGuildsPlayer.voiceClient.is_paused():
            await thisGuildsPlayer.unpause()
        
        if reaction.emoji == "⏭️":
            thisGuildsPlayer.skip()

    
client.run(config["token"])