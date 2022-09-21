import asyncio
from datetime import datetime
import discord
from discord.ext import tasks
import os
import requests
import json
import random
from dotenv import load_dotenv

# load .env file from local
load_dotenv()
# instance of the client
Intents = discord.Intents.default()
Intents.message_content = True
client = discord.Client(intents=Intents)

meme_channel_id = int(os.getenv('MEME_CHANNEL_ID'))

# const
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]
starter_encouragements = [
    "Cheer up!",
    "You can do it!",
    "Hang in there!",
    "You are a star!",
    "You are a great person!"
]
zen_url = "https://zenquotes.io/api/random"
meme_url = "https://meme-api.herokuapp.com/gimme/1"

# method part


def get_quote():
    """
    This function gets a random quote from the API
    return value is {'q': ~~~, 'a': ~~~, 'h': ~~~}
    """
    headers = {'user-agent': 'vscode-restclient'}
    response = requests.request("GET", zen_url, headers=headers)
    json_data = json.loads(response.text)
    if not json_data[0]:
        return "failed fetching data... Anyway, you can do it!!!"
    return json_data[0]


def get_meme():
    """
    This function gets a random meme from the API
    get a jpg or png url
    please refer to this below url
    https://github.com/D3vd/Meme_Api
    """
    response = requests.request("GET", meme_url)
    json_data_for_meme = json.loads(response.text)
    url = json_data_for_meme['memes'][0]['url']
    return url


@tasks.loop(minutes=1.0)
async def show_meme_daily():
    """
    This function sends a meme at 8:00 am everyday.
    This task is called every 1 minutes and if the time is 8:00, it will send meme.
    """
    now = datetime.now().strftime('%H:%M')
    if (now == '08:00'):
        channel = client.get_channel(meme_channel_id)
        await channel.send(f"Good morning! This is today's meme")
        await channel.send(get_meme())
    return


@client.event
async def on_ready():  # when the bot is ready to use
    print(f'We have logged in as {client.user}')
    # "Hey there! I'm your personal assistant. I can help you with anything you need. Just ask me!"


@client.event  # this tells the library we are listening to a message event
async def on_message(message):  # when the bot recieves a message
    # if the message is from the bot (ourselves)
    if message.author == client.user:
        return  # we don't want to reply to ourselves

    # if the message starts with !hello
    if message.content.startswith('!hello'):
        await message.channel.send(f'Hello humans!')  # reply with Hello!
        # await message.author.send('Hello there!') # send a message to the author

    # if the message starts with !inspire
    if message.content.startswith('!inspire'):
        author_name = message.author.name.split()[0]  # get the author's name
        quote = get_quote()
        # await message.channel.send(quote)
        await message.reply(author_name + ", " + quote)

    # if the message contains negative words
    if any(word in message.content for word in sad_words):
        json_data = get_quote()
        quote = json_data['q']
        author = json_data['a']

        await message.channel.send(quote + '- by ' + author)
        await message.channel.send(random.choice(starter_encouragements))

    # identify that as meme channel
    if message.channel.id == meme_channel_id:
        # send a meme to meme channel
        await client.get_channel(meme_channel_id).send(get_meme())


async def main():
    async with client:
        show_meme_daily.start()
        Token = os.getenv('AUTH_TOKEN')
        await client.start(Token)  # run the bot with the token

# Takao implemented this line by using asyncio library insted of client.start(token)
# because show_meme_daily method should be called every 1 minute.
asyncio.run(main())
