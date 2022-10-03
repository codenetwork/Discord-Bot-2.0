import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

from cogs.basics_cog import BasicsCog
from cogs.inspire_cog import InspireCog

BOT = commands.Bot(command_prefix='$')

@BOT.event
async def on_ready():  # when the bot is ready to use
    print(f"We have logged in as {BOT.user}")
    # "Hey there! I'm your personal assistant. I can help you with anything you need. Just ask me!"

async def main():
    async with BOT:
        load_dotenv()
        token = os.getenv("AUTH_TOKEN")
        await BOT.start(token)  # run the bot with the token

BOT.add_cog(BasicsCog(BOT))
BOT.add_cog(InspireCog(BOT))

if __name__ == "__main__":
    asyncio.run(main)
