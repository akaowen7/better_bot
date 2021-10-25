from pytube import YouTube
from pytube import Search

import os
import time

from globals import songList
from song import Song

def OnComputer(messageText):
    if messageText.startswith("https://"):
        id = ""

        try:
            if "https://youtu.be/" in messageText:
                id = messageText.split(" ")[0].split("/")[-1]
            else:
                id = messageText.split(" ")[0].split("=")[-1]
        except:
            return None

        for i in songList:
            if i.songId == id:
                print("Found on computer through id")
                return i    
    else:       
        for i in songList:
            if i.name.lower() in messageText.lower():
                print("Found on computer through search")
                return i
    
    return None

async def OnYoutube(messageText, sentMessage):
    yt = None

    if messageText.startswith("https://"):
        print(f"Trying URL: {messageText}")
        try:
            if "https://youtu.be/" in messageText:
                yt = YouTube(f"https://www.youtube.com/watch?v={messageText.replace('https://youtu.be/', '')}")
            else:
                yt = YouTube(messageText)
        except:
            await sentMessage.edit(content="Invalid URL")
            return None
    else:
        print(f"Searching for: {messageText}")
        results = Search(messageText).results

        if results == None:
            await sentMessage.edit(content=f"There dosent seem to be any results for **{messageText}**")
            return None

        yt = results[0]
    
    compSong = OnComputer(f"https://www.youtube.com/watch?v={yt.vid_info['videoDetails']['videoId']}")
    if compSong != None:
        print("Found on computer after online search")
        return compSong

    streams = yt.streams.filter(only_audio=True).order_by("abr")

    if streams == []:
        await sentMessage.edit(content=f"**{messageText}** dosen't apear to have audio")
        return None

    await sentMessage.edit(content=f"**Downlaoding** `{yt.title}`...")
    stream = streams.last()
    print(f"Started downlaoding '{yt.title}'")
    path = stream.download(os.path.join(os.getcwd(), "songs"), f"{yt.vid_info['videoDetails']['videoId']} {yt.title}.mp3")
    print("Done downlaoding")

    song = Song(path, yt.vid_info['videoDetails']['videoId'], yt.title, yt.thumbnail_url.replace("sddefault", "maxresdefault"), stream.filesize, int(time.time()), yt.length)
    song.addToJson()
    return song