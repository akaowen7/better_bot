import globals

import time
import asyncio


def getFolderSize():
    folderSize = 0
    for i in globals.songList:
        folderSize += i.fileSize
    return folderSize


def checkSongs():
    print("Running cleanup")
    
    songsToBeDeleted = []

    for i in globals.songList:
        if int(time.time()) - i.dateAdded > globals.maxSongDate:
            songsToBeDeleted.append(i)
    
    for i in songsToBeDeleted:
        print(f"{i.name} is old enough to be deleted, deleting...")
        i.delSelf()

    if getFolderSize() > globals.maxSongFolderSize:
        print("Song folder to large, attempting to clear songs")

    s = sorted(globals.songList, key=lambda a: a.dateAdded)
    while getFolderSize() > globals.maxSongFolderSize:
        if s == []:
            print("Cannot delete any files")

        song = s[0]
        if any([song in i.queue for i in globals.players]):
            print(f"{song.name} is in a queue, cannot be deleted")
            s.pop(0)
        else:
            print(f"deleteing {song.name}...")
            song.delSelf()
            s.pop(0)

    print("Done cleanup")
