import os
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

        @bot.command(name="fren")
        async def _fren(ctx):
            """Are u fren?"""
            fren = list(map(int, os.getenv("frens").split()))
            if ctx.author.id in fren:
                await ctx.send("hi fren 👋")
            else:
                await ctx.send("ur not a fren, sawwi 😓")

def setup(bot):
    bot.add_cog(Fun(bot))
