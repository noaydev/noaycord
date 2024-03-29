# Noaycord

#### VIDEO DEMO: <URL>
#### DECRIPTION:
Hello world, I'm Noay_dev and this is Noaycord. A wrapper for the Discord API that's written in Python. It's made as a final project for the CS50x course. After that I will continue updating it hopefully. As of now you have the ability to listen for message events. Nothing much really. I will guide you through how you can do some things with my not so good library.

## Installing and using the library

For now, the only way to use the library is to install it manually. You can't install it through pip. The way to install the library is to download the latest release from [here](https://github.com/noaydev/noaycord/releases), unzip the source code and place the folder inside your working directory. It should look something like this
```
your-folder
|
|--noaycord
|
|--your-app.py
|
|____________
```
where noaycord is the library name. After submitting the project to CS50x I will upload it to PyPI (pip) and it will be installable from there. Way easier then all this.

## Hello world

First here is an example program that prints out hello world when the bot goes online
```py
import noaycord as discord

bot = discord.Bot(discord.get_all_intents())

@bot.on_ready()
async def ready():
    print("Hello world")

bot.run("Token here")
```
Now that's much so let's break it down to different parts.

First we import the noaycord library and "nickname" it as discord. Then we make a new bot class that will have all the discord intents. After that is the function that executes when the bot goes online. It is decorated with the ```bot.on_ready()``` decorator. The function needs to be asynchronous or else it would cause an error, that's why we are using ```async def```. After all that we run the bot with our token that we get from the [Discord Developers Page](https://discord.com/developers/applications).

## Intents

But we can do other things. For example change the intents. We are not limited only to having all the intents. We can choose specific ones to use. That means we can change this:
```py
bot = discord.bot(discord.get_all_intents())
```
to this:

```py
bot = discord.bot([discord.Intents.guild_messages])
```
This snippet allows the bot only to receive events about messages in servers. Here are all intents that the Discord API has: [List of Intents](https://discord.com/developers/docs/topics/gateway#list-of-intents). As of now, Noaycord doesn't support the AUTO_MODERATION_CONFIGURATION and AUTO_MODERATION_EXECUTION intents.

The way you can choose any of these intents is by using their lowercase names. For example the DIRECT_MESSAGE_REACTIONS intent will be direct_message_reactions. Example:

```py
bot = discord.bot([discord.Intents.direct_message_reactions])
```
The intent needs to be in a list because of how the library is designed.

Also there is one thing you need to do before you can choose multiple intents at once. You have to make a list of all intents you want to use.
```py
intents = [
    discord.Intents.guild_messages,
    discord.Intents.direct_messages,
    discord.Intents.guild_message_typing
]
```
Then pass that intent list to the Bot() class

```py
bot = discord.bot(intents)
```

## Messages

Recently added feature, messages. More exactly, message events. This allows our bot to receive messages if they have the guild_messages or direct_messages intents for Server Messages and DMs respectively. Here is how a simple bot that listens for when a message is send works.

```py
import noaycord as discord

intents = [
    discord.Intents.guild_messages,
    discord.Intents.direct_messages
]

bot = discord.Bot(intents)

@bot.on_message()
def message(msg):
    print('message received')

bot.run('Token here')
```
You also have access to basic message's information. You can get the Message ID, Message's Channel ID, Author Information (id, username, display name, tag) and content by using these values respectively
```py
msg.id
msg.channel_id
msg.author.id
msg.author.username
msg.author.display_name
msg.author.discriminator
msg.content
```

Also, you can now reply to messages using ```msg.reply()```. Here is an example:
```py
import noaycord as discord

intents = [
    discord.Intents.guild_messages,
    discord.Intents.direct_messages
]

bot = discord.Bot(intents)

@bot.on_message()
def message(msg):
    msg.reply('Hello world')

bot.run('Token here')
```

> Note that this will cause the bot to get rate limited because it will send too many messages. It will reply to its own messages causing an infinite loop of sorts.

## Files in my project

In the library there are multiple files that serve different purposes. Here all of them will be explained

1. ```__init__.py``` - it tells Python which things to include when importing the library
2. ```.gitignore``` - since this project is built with the help of git, I added a gitignore for git to ignore all files and folders that aren't necessary
3. ```classes.py``` - it contains classes that represent things like Users, Messages, Channels, Servers and so on
4. ```intents.py``` - it contains code for handling intents and contains all intents that the library supports
5. ```methods.py``` - most of the stuff is there. It has things like Identifying, Heartbeats, the Event Loop and the Bot class
6. ```README.md``` - the thing you're reading right now

## Design choices

When I first started making this, I had big design ideas in mind. When I actually got to making all of this, they kinda got behind me. Nonetheless, I present to you, a modern asynchronous Python library that is designed to be "the best there ever was".
