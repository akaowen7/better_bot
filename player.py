import asyncio
import discord

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
        await asyncio.sleep(1.5)
        await self.playNext()
    
    def skip(self):
        self.voiceClient.stop()

    def pause(self):
        self.voiceClient.pause()
    
    def unpause(self):
        self.voiceClient.resume()