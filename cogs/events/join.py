import os
from utilities.database import commit_query
from discord import Member
from discord.ext.commands import Cog, Bot

class OnMemberJoin(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        await commit_query(f'INSERT IGNORE INTO {os.getenv("MYSQL_MEMBER_TABLE")} (id, username) VALUES (%s, %s)', (str(member.id), str(member.name)))

def setup(bot: Bot):
    bot.add_cog(OnMemberJoin(bot))