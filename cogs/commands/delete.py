import discord, os
from discord import Option, ApplicationContext
from discord.ext.commands import Bot, Cog

class Delete(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @discord.slash_command(name="delete", description="Delete messages", guild_ids=[int(os.getenv('TEST_GUILD'))])
    async def gif(self, ctx: ApplicationContext, message_count: Option(int, description="The number of messages to be deleted", min_value=1, max_value=100)):
        await ctx.defer()
        deleted_messages = await ctx.channel.purge(limit=message_count + 1, bulk=True)
        await ctx.channel.send(f"<@{ctx.author.id}> just used /delete command to delete {len(deleted_messages) - 1} messages.")

def setup(bot: Bot):
    bot.add_cog(Delete(bot))