import asyncio
from loguru import logger
from datetime import timedelta, datetime
from discord.ext import tasks
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from config import TIMEZONE

class ReminderTask(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.check_reminder.start()

    def cog_unload(self):
        self.check_reminder.cancel()

    @tasks.loop(count=None, seconds=1)
    async def check_reminder(self):
        now = datetime.now(TIMEZONE).replace(microsecond=0)

        for reminder in self.bot.reminders:
            channel = self.bot.get_channel(int(reminder.channel_id))

            try:
                response_message = await channel.fetch_message(int(reminder.response_id))
            except:
                await reminder.delete(self.bot)
                continue
            
            if reminder.datetime <= now:
                if reminder.datetime == now:
                    await response_message.reply(f"<@{reminder.user_id}> Reminder for this message {reminder.message_url} has been triggered.")

                await reminder.delete(self.bot)

    @check_reminder.before_loop
    async def before_check_reminder(self):
        await self.bot.wait_until_ready()
        now = datetime.now(TIMEZONE)
        next_second = (now + timedelta(seconds=1)).replace(microsecond=0)
        await asyncio.sleep((next_second - now).total_seconds())
        
        
def setup(bot: Bot):
    bot.add_cog(ReminderTask(bot))