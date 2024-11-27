from discord import Member
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from config import GUILD, MEMBER_TABLE

class OnMemberJoin(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        await self.bot.get_guild(GUILD).system_channel.send('Who simply add people in again... smh')
        await self.bot.database.execute(f'INSERT IGNORE INTO {MEMBER_TABLE} (id, username) VALUES (%s, %s)', (str(member.id), str(member.name)))

def setup(bot: Bot):
    bot.add_cog(OnMemberJoin(bot))