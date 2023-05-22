import os
from discord import Guild
from discord.ext.commands import Bot
from utilities.database import retrieve_data, commit_query

async def fetch_members(bot: Bot):
    guild = bot.get_guild(int(os.getenv("TEST_GUILD")))
    user_dict = {}

    query = f'SELECT * FROM {os.getenv("MYSQL_MEMBER_TABLE")} WHERE id IN ('

    notInTableList = []

    for user in guild.members:
        user_dict[user.id] = user.name
        notInTableList.append(user)
        query += f'"{user.id}", '

    query = query[:-2]
    query += ');'

    result = await retrieve_data(query)

    for row in result:
        user_id, _, _ = row

        notInTableList = [user for user in notInTableList if int(user.id) != int(user_id)]

    for user in notInTableList:
        await commit_query(f'INSERT IGNORE INTO {os.getenv("MYSQL_MEMBER_TABLE")} (id, username) VALUES (%s, %s)', (str(user.id), str(user.name)))

    for id, username in user_dict.items():
        await commit_query(f'UPDATE {os.getenv("MYSQL_MEMBER_TABLE")} SET username = %s where id = %s', (str(username), str(id)))