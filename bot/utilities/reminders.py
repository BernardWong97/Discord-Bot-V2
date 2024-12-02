from datetime import datetime, timezone, timedelta
from loguru import logger
from bot.bot_instance import Bot
from config import REMINDER_TABLE

class Reminder():
    def __init__(self, id: str = "", user_id: str = "", response_id: str = "", message_url: str = "", channel_id: str = "", datetime: datetime = datetime.now(timezone(timedelta(hours=8), name="Asia/Kuala_Lumpur"))):
        self.id = id
        self.user_id = user_id
        self.response_id = response_id
        self.message_url = message_url
        self.channel_id = channel_id
        self.datetime = datetime

    async def insert(self, bot: Bot):
        insert_datetime = self.datetime.strftime('%Y-%m-%d %H:%M:%S')
        await bot.database.execute(f'INSERT INTO {REMINDER_TABLE} (user_id, response_id, message_url, channel_id, datetime) VALUES (%s, %s, %s, %s, %s)', (str(self.user_id), str(self.response_id), str(self.message_url), str(self.channel_id), str(insert_datetime)))
        self.id = bot.database.last_id
        bot.reminders.append(self)

    async def delete(self, bot: Bot):
        await bot.database.execute(f'DELETE FROM {REMINDER_TABLE} WHERE id = %s', (str(self.id),))
        bot.reminders.remove(self)

    @staticmethod
    def populate_data(result: tuple):
        id, user_id, response_id, message_url, channel_id, db_datetime = result
        formatted_datetime = db_datetime.replace(tzinfo=timezone(timedelta(hours=8), name='Asia/Kuala_Lumpur'))
        return Reminder(id, user_id, response_id, message_url, channel_id, formatted_datetime)

async def fetch_reminders(bot: Bot):
    logger.info('Fetching Reminders...')
    result = await bot.database.query(f'SELECT * FROM {REMINDER_TABLE};')
    for row in result:
        reminder = Reminder.populate_data(row)
        bot.reminders.append(reminder)

    logger.success('Reminders fetched successfully!')
