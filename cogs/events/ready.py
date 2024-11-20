from utilities.members import fetch_members
from utilities.emojis import fetch_emojis
from discord.ext.commands import Cog, Bot

class OnReady(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}!')

        await fetch_members(self.bot)

        await fetch_emojis(self.bot)
        
        print(f'{self.bot.user.name} is listening for Discord Messages!')

def setup(bot: Bot):
    bot.add_cog(OnReady(bot))