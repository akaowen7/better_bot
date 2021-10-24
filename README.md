# The Better Bot (White People Bangers)

A bot that plays ~~music~~ white people bangers, better then [this bot](https://github.com/cambo602/music_bot). Made using `Python`, using `discord.py[voice]` and `pytube`

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

- v1.0.0 - Made the main.py file, bot plays music and *nothing* else

## TODO

- Fix the songs folder issue of it never deleting the songs and make that more intilegent 
- Skip, pause, queue, and fuckoff options
- Make the messages look better