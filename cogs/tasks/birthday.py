import os
from datetime import time, timezone, timedelta, datetime
from discord import Embed, File
from discord.ext import tasks
from discord.ext.commands import Bot, Cog
from utilities.database import retrieve_data


time_zone = timezone(timedelta(hours=8), name='Asia/Kuala_Lumpur')
task_time = time(hour=0, minute=0, second=0, tzinfo=time_zone)

class Birthday(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.wish_birthday.start()

    @tasks.loop(count=None, time=task_time)
    async def wish_birthday(self):
        today = datetime.now(time_zone).strftime('%m-%d')

        result = await retrieve_data(f"SELECT * FROM {os.getenv('MYSQL_MEMBER_TABLE')} WHERE dob LIKE '%{today}'")

        channel = self.bot.get_channel(int(os.getenv('TEST_CHANNEL')))

        for row in result:
            id, _, _ = row

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
        
def setup(bot: Bot):
    bot.add_cog(Birthday(bot))