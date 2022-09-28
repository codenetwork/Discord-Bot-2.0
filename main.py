import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

BOT = commands.Bot()

@BOT.event
async def on_ready():  # when the bot is ready to use
    print(f"We have logged in as {BOT.user}")
    # "Hey there! I'm your personal assistant. I can help you with anything you need. Just ask me!"

async def main():
    async with BOT:
        load_dotenv()
        token = os.getenv("AUTH_TOKEN")
        await BOT.start(token)  # run the bot with the token

if __name__ == "__main__":
    asyncio.run(main)
