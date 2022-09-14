import discord
import os
import requests
import json
import random

# instance of the client
Intents = discord.Intents.default()
# Intents.message_content = True
client = discord.Client(intents=Intents)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
    "Cheer up!", 
    "You can do it!",
    "Hang in there!",
    "You are a star!",
    "You are a great person!"
]

def get_quote():
    """
    This function gets a random quote from the API
    """
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return quote

@client.event
async def on_ready(): # when the bot is ready to use
    print(f'We have logged in as {client.user}')
    # "Hey there! I'm your personal assistant. I can help you with anything you need. Just ask me!"

@client.event # this tells the library we are listening to a message event
async def on_message(message): # when the bot recieves a message
    if message.author == client.user: # if the message is from the bot (ourselves)
        return # we don't want to reply to ourselves

    if message.content.startswith('!hello'): # if the message starts with !hello
        await message.channel.send(f'Hello humans!') # reply with Hello!
        # await message.author.send('Hello there!') # send a message to the author
    
    if message.content.startswith('!inspire'): # if the message starts with !inspire
        author_name = message.author.name.split()[0] # get the author's name
        quote = get_quote()
        # await message.channel.send(quote)
        await message.reply(author_name + ", " + quote)
    
    if any(word in message.content for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))
        # message.channel.send("I'm sorry to hear that. I'm always here to help!")

Token  = os.getenv('AUTH_TOKEN')
client.run(Token) # run the bot with the token 