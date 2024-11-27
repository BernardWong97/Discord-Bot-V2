from discord import DiscordException
from discord.ext.commands import Cog, Context, CommandNotFound
from bot.bot_instance import Bot

class OnCommandError(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, context: Context, exception: DiscordException):
        if isinstance(exception, CommandNotFound):
            return
        
        return await super().on_command_error(context, exception)

def setup(bot: Bot):
    bot.add_cog(OnCommandError(bot))