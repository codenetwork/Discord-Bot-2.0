from discord.ext import commands
import requests
import random

SAD_WORDS = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

STARTER_ENCOURAGEMENTS = [
    "Cheer up!",
    "You can do it!",
    "Hang in there!",
    "You are a star!",
    "You are a great person!",
]

def get_quote() -> str:
    """
    This function gets a random quote from the API
    """
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    json_data = response.json()
    quote = json_data[0]["q"] + " - " + json_data[0]["a"]
    return quote


class InspireCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def inspire(self, ctx: commands.Context):
        author_name = ctx.author.name.split()[0]  # get the author's name
        quote = get_quote()
        # await message.channel.send(quote)
        await ctx.reply(author_name + ", " + quote)

    @commands.Cog.listener()
    async def sad_reply(self, ctx: commands.Context):
        if any(word in ctx.message.content.lower() for word in SAD_WORDS):
            await ctx.channel.send(random.choice(STARTER_ENCOURAGEMENTS))
        # message.channel.send("I'm sorry to hear that. I'm always here to help!")
