import json
import os
from globals import songList

class Song():
    def __init__(self, filePath, songId, name, thumbnail, fileSize, dateAdded, length, neverDelete):
        self.filePath = filePath
        self.songId = songId
        self.name = name
        self.thumbnail = thumbnail
        self.fileSize = fileSize
        self.dateAdded = dateAdded
        self.length = length
        self.neverDelete = neverDelete

    def __str__(self):
        return f"{self.name}, {self.songId}"

    def __repr__(self):
        return f"{self.name}, {self.songId}"

    def rewriteJson(self):
        tempList = [{"filePath": i.filePath, "songId": i.songId, "name": i.name, "thumbnail": i.thumbnail, "fileSize": i.fileSize, "dateAdded": i.dateAdded, "length": i.length, "neverDelete": i.neverDelete} for i in songList]
        data = {}
        data["songs"] = tempList
        json.dump(data, open('song_list.json', 'w'), indent=4)

    def addToJson(self):
        songList.append(self)
        self.rewriteJson()

    def delSelf(self):
        os.remove(self.filePath)
        songList.remove(self)
        self.rewriteJson()