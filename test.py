import json
import os

from pytube import YouTube
from pytube import Search

yt = YouTube("https://youtu.be/Qw5s4AM3JpA")
t = yt.streams.filter(only_audio=True).order_by("abr")

# t[0].download(os.path.join(os.getcwd(), "songs"), f"{yt.vid_info['videoDetails']['videoId']}.mp3")
# print("Done")
