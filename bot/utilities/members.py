from loguru import logger
from bot.bot_instance import Bot
from config import GUILD, MEMBER_TABLE

async def fetch_members(bot: Bot):
    logger.info('Fetching members...')
    guild = bot.get_guild(GUILD)
    user_dict = {}

    query = f'SELECT id, username FROM {MEMBER_TABLE} WHERE id IN ('

    notInTableList = []

    for user in guild.members:
        user_dict[user.id] = user.name
        notInTableList.append(user)
        query += f'"{user.id}", '

    query = query[:-2]
    query += ');'

    result = await bot.database.query(query)

    for row in result:
        user_id, _ = row

        notInTableList = [user for user in notInTableList if int(user.id) != int(user_id)]

    for user in notInTableList:
        await bot.database.execute(f'INSERT IGNORE INTO {MEMBER_TABLE} (id, username) VALUES (%s, %s)', (str(user.id), str(user.name)))

    for id, username in user_dict.items():
        await bot.database.execute(f'UPDATE {MEMBER_TABLE} SET username = %s where id = %s', (str(username), str(id)))

    logger.success('Members fetched successfully!')