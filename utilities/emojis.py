import os
from discord import Guild
from discord.ext.commands import Bot
from utilities.database import retrieve_data, commit_query

async def fetch_emojis(bot: Bot):
    print('Fetching Emojis...')
    guild = bot.get_guild(int(os.getenv("GUILD")))
    emoji_dict = {}

    query = f'SELECT * FROM {os.getenv("MYSQL_EMOJI_TABLE")} WHERE id IN ('

    notInTableList = []

    for emoji in guild.emojis:
        emoji_dict[emoji.id] = emoji.name
        notInTableList.append(emoji)
        query += f'"{emoji.id}", '

    query = query[:-2]
    query += ');'

    result = await retrieve_data(query)

    for row in result:
        emoji_id, _, _ = row

        notInTableList = [emoji for emoji in notInTableList if int(emoji.id) != int(emoji_id)]

    for emoji in notInTableList:
        await commit_query(f'INSERT IGNORE INTO {os.getenv("MYSQL_EMOJI_TABLE")} (id, name, data) VALUES (%s, %s, %s)', (str(emoji.id), str(emoji.name), f"<:{emoji.name}:{emoji.id}>"))

    for id, name in emoji_dict.items():
        await commit_query(f'UPDATE {os.getenv("MYSQL_EMOJI_TABLE")} SET name = %s, data = %s where id = %s', (str(name), str(id), f"<:{name}:{id}>"))

async def get_emoji_data(emoji_name: str):
    result = await retrieve_data(f'SELECT data FROM emojis WHERE name = "{emoji_name}";')
    return result[0][0]