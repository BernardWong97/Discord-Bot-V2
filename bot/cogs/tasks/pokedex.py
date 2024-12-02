from datetime import time
from discord.ext import tasks
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from config import TIMEZONE

task_time = time(hour=0, minute=0, second=0, tzinfo=TIMEZONE)

class Pokedex(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.update_pokedex.start()

    def cog_unload(self):
        self.update_pokedex.cancel()

    @tasks.loop(count=None, time=task_time)
    async def update_pokedex(self):
        await self.bot.pokedex.get_all_data()
        
def setup(bot: Bot):
    bot.add_cog(Pokedex(bot))