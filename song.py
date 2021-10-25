import json
from globals import songList

class Song():
    def __init__(self, filePath, songId, name, thumbnail, fileSize, dateAdded):
        self.filePath = filePath
        self.songId = songId
        self.name = name
        self.thumbnail = thumbnail
        self.fileSize = fileSize
        self.dateAdded = dateAdded

    def addToJson(self):
        songList.append(self)

        tempList = [{"filePath": i.filePath, "songId": i.songId, "name": i.name, "thumbnail": i.thumbnail, "fileSize": i.fileSize, "dateAdded": i.dateAdded} for i in songList]
        data = {}
        data["songs"] = tempList
        json.dump(data, open('song_list.json', 'w'), indent=4)