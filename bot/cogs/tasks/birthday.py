from datetime import time, datetime
from discord import Embed, File
from discord.ext import tasks
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from config import TIMEZONE, MEMBER_TABLE, ALL_CHAT_CHANNEL

task_time = time(hour=0, minute=0, second=0, tzinfo=TIMEZONE)

class Birthday(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.wish_birthday.start()

    def cog_unload(self):
        self.wish_birthday.cancel()

    @tasks.loop(count=None, time=task_time)
    async def wish_birthday(self):
        today = datetime.now(TIMEZONE).strftime('%m-%d')

        result = await self.bot.database.query(f"SELECT id FROM {MEMBER_TABLE} WHERE dob LIKE '%{today}'")

        channel = self.bot.get_channel(ALL_CHAT_CHANNEL)

        for row in result:
            id = row[0]

            user = channel.guild.get_member(int(id))

            embed_message = Embed(
                title=f"**Happy Birthday {user.display_name}**",
                description=f"Happy Birthday to our beloved member **{user.display_name}**!",
                color=0xFF0000,
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            )

            embed_message.set_image(url='attachment://birthday.gif')

            file_name = "./attachments/birthday.gif"
                    
            with open(file_name, 'rb') as f:
                attachment = File(f, filename="birthday.gif")

                await channel.send(f"<@{id}>", embed=embed_message, file=attachment)

    @wish_birthday.before_loop
    async def before_wish_birthday(self):
        await self.bot.wait_until_ready()
        
def setup(bot: Bot):
    bot.add_cog(Birthday(bot))