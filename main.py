import discord
import json
import os
import asyncio
import time

from pytube import YouTube
from pytube import Search

config = json.load(open("config.json"))

client = discord.Client()

players = []
songList = []

class Song():
    def __init__(self, filePath, songId, name, thumbnail, fileSize, dateAdded):
        self.filePath = filePath
        self.songId = songId
        self.name = name
        self.thumbnail = thumbnail
        self.fileSize = fileSize
        self.dateAdded = dateAdded

        songList.append(self)

        tempList = [{"filePath": i.filePath, "songId": i.songId, "name": i.name, "thumbnail": i.thumbnail, "fileSize": i.fileSize, "dateAdded": i.dateAdded} for i in songList]
        data = {}
        data["songs"] = tempList
        json.dump(data, open('song_list.json', 'w'))

if not os.path.isfile("./song_list.json"):
    data = {}
    data["songs"] = []
    with open('song_list.json', 'w') as outfile:
        json.dump(data, outfile)

jsonSongList = json.load(open("song_list.json"))["songs"]

for i in jsonSongList:
    songList.append(Song(i["filePath"], i["songId"], i["name"], i["thumbnail"], i["fileSize"], i["dateAdded"]))

class Player():
    def __init__(self, guild, queue, channel):
        self.guild = guild
        self.queue = queue
        self.channel = channel
        self.player = None
        self.voiceClient = None
        self.next = asyncio.Event()

    def afterPlay(self, e):
        print(f"Done playing {self.queue[0].name}\nException: ", e)
        self.queue.pop(0)
        self.next.set()

    async def playNext(self):  
        while True:
            self.next.clear()

            if self.queue == []:
                await self.voiceClient.disconnect() 
                players.remove(self)
                break
                # del self

            print(f"Playing {self.queue[0].name}")        
            await self.channel.send(f"Playing **{self.queue[0].name}**")
            self.voiceClient.play(discord.FFmpegPCMAudio(self.queue[0].filePath), after=self.afterPlay)

            await self.next.wait()
    
    async def joinAndPlay(self, message):
        self.voiceClient = await message.author.voice.channel.connect()
        await self.playNext()

def SearchSongsOnComputer(id, searchTerms):
    # ToDo
    return

async def getSong(message, thisGuildsPlayer):
    if len(message.content) < 2:
        return await message.channel.send(f"You have to put what you want to play after the command! Like `{config['prefix']}play fly me to the moon`")

    if (message.author.voice == None):
        return await message.channel.send("*You have to be in a voice channel to do that command*")

    messageText = " ".join(message.content.split(" ")[1:])
    yt = None

    if messageText.startswith("https://"):
        print(f"Trying URL: {messageText}")
        try:
            if "https://youtu.be/" in messageText:
                yt = YouTube(f"https://www.youtube.com/watch?v={messageText.replace('https://youtu.be/', '')}")
            else:
                yt = YouTube(messageText)
        except:
            return await message.channel.send("Invalid URL")
    else:
        print(f"Searching for: {messageText}")
        results = Search(messageText).results

        if results == None:
            return await message.channel.send(f"There dosent seem to be any results for **{messageText}**")

        yt = results[0]

    streams = yt.streams.filter(only_audio=True).order_by("abr")

    if streams == []:
        return await message.channel.send(f"**{messageText}** dosen't apear to have audio")

    stream = streams.last()
    print(f"Started downlaoding '{yt.title}'")
    path = stream.download(os.path.join(os.getcwd(), "songs"), f"{yt.vid_info['videoDetails']['videoId']} {yt.title}.mp3")
    print("Done downlaoding")

    song = Song(path, yt.vid_info['videoDetails']['videoId'], yt.title, yt.thumbnail_url.replace("sddefault", "maxresdefault"), stream.filesize, int(time.time()))

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