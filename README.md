# The Better Bot (White People Bangers) v3.0.0 Alpha

A bot that plays ~~music~~ white people bangers, better then [this bot](https://github.com/cambo602/music_bot). Made using `Python`, with `discord.py[voice]` and `pytube`

# Getting started

Clone the repo and navigate to it, and then install these dependencies:

    pip install discord.py[voice] pytube

The bots token and prefix are stored in a file called `config.json` located in main folder. Make it, and fill it with this:

    {
        "token": "YOUR_TOKEN_HERE",
        "prefix": "YOUR_PREFIX_HERE"
    }

And then fill in the values for your bot's prefix and the [bots token](https://discord.com/developers/applications)

Run the bot with this command (in the bots directiory):

    python main.py

Also as of right now you need to make a folder called `songs` in the `better_bot` folder, this will be populated with songs, and it never deletes them! (yet)

## Version Changes

- v3.0.0 - MultiFile, decided that this project was currently in alpha
- v2.0.1 - shit the test.py was not suposed to be there
- v2.0.0 - bot now saves the files and downlads inteligently
- v1.1.0 - It can play more then one song, also the song_list.json is broken
- v1.0.0 - Made the main.py file, bot plays music and *nothing* else

## TODO

- Skip, pause, queue, and fuckoff options
- Make the messages look better
- M U L T I F I L E