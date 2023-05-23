from utilities.members import fetch_members
from discord import Member
from discord.ext.commands import Cog, Bot

class OnMemberJoin(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        await fetch_members(self.bot)
        print(f'Hello {member.name}')

def setup(bot: Bot):
    bot.add_cog(OnMemberJoin(bot))