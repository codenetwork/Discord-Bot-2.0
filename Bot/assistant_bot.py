import discord
import os
import requests
import json
import random
from dotenv import load_dotenv

# instance of the client
Intents = discord.Intents.default()
Intents.message_content = True
client = discord.Client(intents=Intents)

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


def get_quote():
    """
    This function gets a random quote from the API(zenquotes)
    API references is below.
    (https://zenquotes.io/)
    return value is {'q': ~~~, 'a': ~~~, 'h': ~~~}
    """
    headers = {'user-agent': 'vscode-restclient'}
    response = requests.request("GET", zen_url, headers=headers)
    json_data = json.loads(response.text)
    if not json_data[0]:
        return "failed fetching data... Anyway, you can do it!!!"
    return json_data[0]


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
        json_data = get_quote()
        quote = json_data['q']
        # await message.channel.send(quote)
        await message.reply(author_name + ", " + quote)

    # if the message contains negative words("sad", "depressed", "unhappy", "angry", "miserable", "depressing")
    # return a sentence that can motivate the user
    if any(word in message.content for word in sad_words):
        json_data = get_quote()
        quote = json_data['q']
        author = json_data['a']

        await message.channel.send(quote + '- by ' + author)
        await message.channel.send(random.choice(starter_encouragements))

load_dotenv()
Token = os.getenv('AUTH_TOKEN')
client.run(Token)  # run the bot with the token
