from loguru import logger
from bot.utilities import members, emojis, reminders
from discord.ext.commands import Cog
from bot.bot_instance import Bot

class OnReady(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        logger.success(f'Logged in as {self.bot.user}!')

        await self.bot.connect_database()

        await members.fetch_members(self.bot)

        await emojis.fetch_emojis(self.bot)

        await reminders.fetch_reminders(self.bot)

        logger.success(f'{self.bot.user.name} is listening for Discord Messages!')

def setup(bot: Bot):
    bot.add_cog(OnReady(bot))