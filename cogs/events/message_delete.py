import os
from utilities.emojis import get_emoji_data
from discord import Message, AuditLogAction
from discord.ext.commands import Cog, Bot

class OnMessageDelete(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        if message.author.bot:
            return

        test_channel = self.bot.get_channel(int(os.getenv('TEST_CHANNEL')))

        async for entry in message.guild.audit_logs(limit=1, action=AuditLogAction.message_delete):
            user = entry.user

            await test_channel.send(f"<@{user.id}> deleted a message at <#{message.channel.id}>:\n`{message.author.display_name}: {message.content}`")

def setup(bot: Bot):
    bot.add_cog(OnMessageDelete(bot))