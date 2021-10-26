import globals

import time
import asyncio

def getFolderSize():
    folderSize = 0
    for i in globals.songList:
        folderSize += i.fileSize
    return folderSize

async def checkSongs():
    while True:
        for i in globals.songList:
            if int(time.time()) - i.dateAdded > globals.maxSongDate:
                i.delSelf()
        
        # UNSAFE HUGE ISSUE
        while getFolderSize() > globals.maxSongFolderSize:
            s = sorted(globals.songList, key=lambda a: a.dateAdded)
            s[0].delSelf()

        await asyncio.sleep(15)

asyncio.run(checkSongs())