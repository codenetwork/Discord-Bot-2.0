from discord.ext import commands


class BasicsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def hello(self, ctx: commands.Context):
        await ctx.channel.send(f"Hello humans!")  # reply with Hello!
        # await message.author.send('Hello there!') # send a message to the author
