from discord import Message
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from config import OWNER_ID

class OnMessageUpdate(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if before.author.bot:
            return
        
        owner = await self.bot.get_or_fetch_user(OWNER_ID)

        await owner.send(f"<@{after.author.id}> edited a message at <#{after.channel.id}>:\nBefore: `{before.content}`\nAfter: `{after.content}`")

def setup(bot: Bot):
    bot.add_cog(OnMessageUpdate(bot))