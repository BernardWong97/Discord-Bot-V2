from discord import Message, AuditLogAction
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from config import OWNER_ID

class OnMessageDelete(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        if message.author.bot:
            return

        async for entry in message.guild.audit_logs(limit=1, action=AuditLogAction.message_delete):
            user = entry.user

            owner = await self.bot.get_or_fetch_user(OWNER_ID)

            await owner.send(f"<@{user.id}> deleted a message at <#{message.channel.id}>:\n`{message.author.display_name}: {message.content}`")

def setup(bot: Bot):
    bot.add_cog(OnMessageDelete(bot))