import asyncio
import discord
import datetime

from globals import players

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

    def playingEmbed(self, song):
        emb = discord.Embed(title = song.name, description = f"Length: {str(datetime.timedelta(seconds=song.length)).lstrip('0:')}", color=0x1CB8B1)
        emb.set_author(name="Now Playing", icon_url="https://cdn.discordapp.com/avatars/654147464357609519/03a12bea6dc1d7600fb41c0317445f4a.png?size=4096")
        emb.set_thumbnail(url=song.thumbnail)
        return emb

    async def playNext(self):  
        while True:
            self.next.clear()

            if self.queue == []:
                await self.voiceClient.disconnect() 
                players.remove(self)
                break
                # del self

            print(f"Playing {self.queue[0].name}")        
            audio = discord.FFmpegPCMAudio(self.queue[0].filePath)
            await asyncio.sleep(1.2)
            self.voiceClient.play(audio, after=self.afterPlay)
            
            sent = await self.channel.send(embed=self.playingEmbed(self.queue[0]))
            for i in ["⏸", "⏭️"]:
                await sent.add_reaction(i)

            await self.next.wait()
    
    async def joinAndPlay(self, message, sentMessage):
        self.voiceClient = await message.author.voice.channel.connect()
        await sentMessage.delete(delay=.8)
        await self.playNext()
    
    async def skip(self, message):
        self.voiceClient.stop()
        await message.add_reaction("👍")

    async def pause(self, message):
        self.voiceClient.pause()
        await message.channel.send("**Paused**, send the `play` command to resume")
    
    async def unpause(self, message):
        self.voiceClient.resume()
        await message.add_reaction("👍")

    async def sendQueue(self, message):
        if self.queue == []:
            # This should never happen
            await message.channel.send("**The queue is empty**")

        emb = discord.Embed(title = "Queue", description = "", color=0x1CB8B1)
        emb.set_author(name=self.guild.name, icon_url="https://cdn.discordapp.com/avatars/654147464357609519/03a12bea6dc1d7600fb41c0317445f4a.png?size=4096")
        emb.add_field(name="Now PLaying:", value=f"`{self.queue[0].name}` - Length: {self.queue[0].length}", inline=False)

        j = 0
        for i in self.queue[1:]:
            if j > 10:
                emb.add_field(value=f"And {len(self.queue) - 10} more other songs", name="\u200b", inline=False)
                break
            
            emb.add_field(value=f"{self.queue.index(i) + 1}. `{i.name}` - Length: {i.length}", name="\u200b", inline=False)
            j += 1

        await message.channel.send(embed=emb)