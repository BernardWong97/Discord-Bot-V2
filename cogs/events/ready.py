from utilities.members import fetch_members
from discord import Member
from discord.ext.commands import Cog, Bot

class OnReady(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}!')
        print(f'{self.bot.user.name} is listening for Discord Messages!')

        await fetch_members(self.bot)

def setup(bot: Bot):
    bot.add_cog(OnReady(bot))