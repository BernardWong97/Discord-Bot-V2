import os, random
from utilities.database import retrieve_data
from discord import Message, File
from discord.ext.commands import Cog, Bot
from typing import Union

class OnMessage(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        reply_list = []
        file_list = []

        if message.author.bot:
            return
        
        if "@here" in message.content or "@everyone" in message.content:
            return

        if message.reference is not None:
            return
        
        if message.channel.id in [int(os.getenv('ALL_CHAT_CHANNEL')), int(os.getenv('TEST_CHANNEL'))]:
            for mentioned_user in message.mentions:
                if mentioned_user.id == int(os.getenv('TEST_BOT_ID')):
                    if message.author.id == int(os.getenv('BERD_ID')):
                        quote = await self._get_special_quote()

                        reply_list.append(quote)
                    else:
                        quote = await self._get_quote(mentioned_user.id)

                        if isinstance(quote, str):
                            reply_list.append(quote)
                        else:
                            file_list.append(quote)
                elif not mentioned_user.bot:
                    quote = await self._get_quote(mentioned_user.id)

                    if isinstance(quote, str):
                        reply_list.append(quote)
                    else:
                        file_list.append(quote)

        if len(reply_list) != 0:
            quote = "\n".join(reply_list)
            await message.reply(quote)
        
        if len(file_list) != 0:
            for f in file_list:
                await message.reply(file=f)

    async def _get_quote(self, id: str) -> Union[File, str]:
        result = await retrieve_data(f'SELECT * FROM {os.getenv("MYSQL_QUOTE_TABLE")} WHERE member_id = "{id}";')
        
        if len(result) == 0:
            return f'<@{os.getenv("BERD_ID")}> 沒有教我要怎樣應<@{id}>gok...'
        else:
            _, _, quote = result[random.randint(0, len(result) - 1)]

            if str(quote).startswith("Attachment"):
                file_name = "./attachments/" + str(quote).split("-")[1]
                
                with open(file_name, 'rb') as f:
                    attachment = File(f)
                    return attachment
            else:
                return quote

    async def _get_special_quote(self) -> str:
        result = await retrieve_data(f'SELECT * FROM {os.getenv("MYSQL_QUOTE_TABLE")} WHERE member_id = "SPECIAL";')
        _, _, quote = result[random.randint(0, len(result) - 1)]

        return quote


def setup(bot: Bot):
    bot.add_cog(OnMessage(bot))