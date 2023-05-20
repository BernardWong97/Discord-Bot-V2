import discord, os
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="Ping Here pls", guild_ids=[int(os.getenv('TEST_GUILD'))])
    async def test_command(self, ctx: commands.Context):
        await ctx.respond("Pong!")

def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))