import os
from utilities.prompt import prompt
from discord import Message
from discord.ext.commands import Cog
from bot import Bot

class OnMessage(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):

        if message.author.bot:
            return
        
        if "@here" in message.content or "@everyone" in message.content:
            return

        if message.reference is not None:
            return
        
        if message.channel.id == int(os.getenv('ALL_CHAT_CHANNEL')):
            if int(os.getenv('BOT_ID')) in [mention.id for mention in message.mentions]:
                content = message.content.replace(f"<@{int(os.getenv('BOT_ID'))}>", "").strip()
                message.content = content.strip()

                await message.channel.trigger_typing()
                response = await prompt(self.bot, message)

                await message.reply(response)


def setup(bot: Bot):
    bot.add_cog(OnMessage(bot))