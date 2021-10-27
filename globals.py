# These are where the bot stores info, no touch
songList = []
players = []

# These are settings you can change

# Max length of time to keep a song downlaoded 
# since it was last used (In seconds (I'm sorry))
# default: 1 week (604800 seconds)
maxSongDate = 604800

# Max size of the song folder before it starts
# before it starts deleting songs (In bytes)
# default: 500mb (524288000 bytes)
maxSongFolderSize = 524288000

# Max length of a song it will download (in seconds)
# default: 2 hours (7200 seconds)
maxSongLength = 7200