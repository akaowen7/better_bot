import discord
import json
import os

from pytube import YouTube
from pytube import Search

config = json.load(open("config.json"))
client = discord.Client()

players = []

class Song():
    def __init__(self, filePath, name, thumbnail):
        self.filePath = filePath
        self.name = name
        self.thumbnail = thumbnail

class Player():
    def __init__(self, guild, queue, channel):
        self.guild = guild
        self.queue = queue
        self.channel = channel
        self.player = None
        self.voiceClient = None

    async def playNext(self):  
        if self.queue == []:
            players.remove(self)
            self.voiceClient.disconnect()
            del self
            return # not sure if this will happen

        async def afterPlay(e):
            print(f"Done playing {queue[0].name}\nException: ", e)
            await self.voiceClient.disconnect()
            self.queue.pop(0)
            await playNext()

        print(f"Playing {self.queue[0].name}")
        self.voiceClient.play(discord.FFmpegPCMAudio(self.queue[0].filePath), after=lambda e: afterPlay(e))
        return await self.channel.send(f"Playing *{self.queue[0].name}*")
    
    async def joinAndPlay(self, message):
        user = message.author
        if (user.voice.channel == None):
            return await message.channel.send("You Have to be in a voice channel")

        self.voiceClient = await user.voice.channel.connect()

        await self.playNext()


async def getSong(message):
    if len(message.content) < 2:
        return await message.channel.send(f"You have to put want you want to play after the command! Like `{config['prefix']}play fly me to the moon`")

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

    t = yt.streams.filter(only_audio=True)
    print(f"Started downlaoding '{yt.title}'")
    path = t[0].download(os.path.join(os.getcwd(), "songs"), f"{yt.vid_info['videoDetails']['videoId']}.mp3")
    print("Done downlaoding")

    song = Song(path, yt.title, yt.thumbnail_url)
    
    thisGuildsPlayer = None
    for i in players:
        if i.guild == message.guild:
            thisGuildsPlayer = i
            break

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

    if args[0] == "play" or args[0] == "p":
        await getSong(message)
    else:
        await message.channel.send(f"Not a command {args}")
    
client.run(config["token"])