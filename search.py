from pytube import YouTube
from pytube import Search

import os
import time

from globals import songList
from globals import maxSongLength
from song import Song
from manageSongs import checkSongs

def OnComputer(messageText):
    for i in songList:
        if i.songId in messageText or i.songId == messageText:
            print("Found on computer through id")
            i.dateAdded = int(time.time())
            i.rewriteJson()
            return i  
        if i.name.lower() in messageText.lower():
            print("Found on computer through search")
            i.dateAdded = int(time.time())
            i.rewriteJson()
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
    
    compSong = OnComputer(yt.vid_info['videoDetails']['videoId'])

    if compSong != None:
        print("Found on computer after online search")
        return compSong

    streams = yt.streams.filter(only_audio=True).order_by("abr")

    if streams == []:
        await sentMessage.edit(content=f"**{messageText}** dosen't apear to have audio")
        return None

    if yt.length > maxSongLength:
        print("Song was too long")
        await sentMessage.edit(content=f"*The video I found is over 2 hours. So, uh, no*")
        return None

    await sentMessage.edit(content=f"**Downlaoding** `{yt.title}`...")
    stream = streams.last()
    print(f"Started downlaoding '{yt.title}'")
    path = stream.download(os.path.join(os.getcwd(), "songs"), f"{yt.vid_info['videoDetails']['videoId']}.mp3")
    print("Done downlaoding")

    checkSongs()

    song = Song(path, yt.vid_info['videoDetails']['videoId'], yt.title, yt.thumbnail_url.replace("sddefault", "maxresdefault"), stream.filesize, int(time.time()), yt.length, False)
    song.addToJson()
    return song