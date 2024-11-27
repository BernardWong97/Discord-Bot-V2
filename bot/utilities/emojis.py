import os
from loguru import logger
from bot.bot_instance import Bot
from config import GUILD, EMOJI_TABLE

async def fetch_emojis(bot: Bot):
    logger.info('Fetching Emojis...')
    guild = bot.get_guild(GUILD)
    emoji_dict = {}

    query = f'SELECT * FROM {EMOJI_TABLE} WHERE id IN ('

    notInTableList = []

    for emoji in guild.emojis:
        emoji_dict[emoji.id] = emoji.name
        notInTableList.append(emoji)
        query += f'"{emoji.id}", '

    query = query[:-2]
    query += ');'

    result = await bot.database.query(query)

    for row in result:
        emoji_id, _, _ = row

        notInTableList = [emoji for emoji in notInTableList if int(emoji.id) != int(emoji_id)]

    for emoji in notInTableList:
        await bot.database.execute(f'INSERT IGNORE INTO {EMOJI_TABLE} (id, name, data) VALUES (%s, %s, %s)', (str(emoji.id), str(emoji.name), f"<:{emoji.name}:{emoji.id}>"))

    for id, name in emoji_dict.items():
        await bot.database.execute(f'UPDATE {EMOJI_TABLE} SET name = %s, data = %s where id = %s', (str(name), str(id), f"<:{name}:{id}>"))

    logger.success('Emojis fetched successfully!')