import os
from utilities.emojis import get_emoji_data
from discord import Message
from discord.ext.commands import Cog, Bot

class OnMessageUpdate(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if before.author.bot:
            return
        
        test_channel = self.bot.get_channel(int(os.getenv('TEST_CHANNEL')))

        await test_channel.send(f"<@{after.author.id}> edited a message at <#{after.channel.id}>:\nBefore: `{before.content}`\nAfter: `{after.content}`")

def setup(bot: Bot):
    bot.add_cog(OnMessageUpdate(bot))