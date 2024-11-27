import os
from discord import Message
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from langchain_core.messages import HumanMessage
from config import BOT_ID, ALL_CHAT_CHANNEL, QUOTE_TABLE, MEMBER_TABLE

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
            ref_message = message.reference.resolved

            if ref_message.author.id == BOT_ID:
                content = message.content.replace(f"<@{BOT_ID}>", "").strip()
                message.content = content.strip()

                await message.channel.trigger_typing()
                response = await self.__generate_response(message)

                await message.reply(response)
            return
        
        if message.channel.id == ALL_CHAT_CHANNEL:
            if BOT_ID in [mention.id for mention in message.mentions]:
                content = message.content.replace(f"<@{BOT_ID}>", "").strip()
                message.content = content.strip()

                await message.channel.trigger_typing()
                response = await self.__generate_response(message)

                await message.reply(response)
            return
        
    async def __generate_response(self, message: Message):
        role_message = "Reply like a friend."

        result = await self.bot.database.query(f'SELECT * FROM {QUOTE_TABLE} WHERE member_id = {message.author.id};')

        quote_messages = []

        for row in result:
            _, _, quote = row

        if quote is not None:
            quote_messages.append("\"" + quote + "\"")

        result = await self.bot.database.query(f'SELECT role_message FROM {MEMBER_TABLE} WHERE id = {message.author.id};')

        if len(result) > 0:
            if (result[0][0] is not None):
                role_message = result[0][0]

        role_message += f" Here are some examples that you will reply: "

        if len(quote_messages) > 0:
            role_message += ", ".join(quote_messages)
        else:
            quote_array = ["Why do you tag me?", "什麽事情啊？", "叫我嗎?", "???", "做莫"]
            role_message += ", ".join(quote_array)

        input_messages = [HumanMessage(content=message.content)]
        return await self.bot.ai.prompt(input_messages, role_message, message.author.id)

def setup(bot: Bot):
    bot.add_cog(OnMessage(bot))