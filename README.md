# The Better Bot v3.1.1 Alpha

A discord bot that plays music, better then [this bot](https://github.com/cambo602/music_bot). Made using `Python`, with `discord.py[voice]` and `pytube` becasue of issues with javascript plugins on the [older bot](https://github.com/cambo602/music_bot)

Apparently it only works with `Python 3.8`? (Because of `PyNaCl`)

## Features

- This bot runs on discord, and plays music when you're in a voice call. Audio is downloaded from YouTube, and played through discord.
- It has "lots" of cool high-tech commands like "play", "pause" and "skip"!
Has a queue that gets added to as you request songs
- You can control it via emotes under its messages (techicanly a GIU if you squint!!!)

# Getting started

Clone the repo and navigate to it, and then install these dependencies:

    pip install discord.py[voice] pytube

The bots token and prefix are stored in a file called `config.json` located in main folder. Make it, and fill it with this:
~~~json
{
    "token": "YOUR_TOKEN_HERE",
    "prefix": "YOUR_PREFIX_HERE"
}
~~~
And then fill in the values for your bot's prefix and the [bots token](https://discord.com/developers/applications)

Run the bot with this command (in the bots directiory):

    python main.py

# Version Changes

- v3.1.1 - Preped to allow for the addition of more commands, went public (done with heroku), updated `README.md`
- v3.1.0 - Reactions work, all is functional
- v3.0.0 - Multi-file, decided that this project was currently in alpha
- v2.0.1 - The `test.py` was not suposed to be there
- v2.0.0 - Bot now saves the files and downlads inteligently
- v1.1.0 - It can play more then one song, also the song_list.json is broken
- v1.0.0 - Made the `main.py` file, bot plays music and *nothing* else

# TODO

- more functions?
- better file managemnt?
- soundcloud
- playlists