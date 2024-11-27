import discord
from discord import Option, ApplicationContext
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from config import GUILD

class Delete(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @discord.slash_command(name="delete", description="Delete messages", guild_ids=[GUILD])
    async def delete(self, ctx: ApplicationContext, message_count: Option(int, description="The number of messages to be deleted", min_value=1, max_value=100)):
        await ctx.defer()
        deleted_messages = await ctx.channel.purge(limit=message_count + 1, bulk=True)
        message = f"<@{ctx.author.id}> just used /delete command to delete {len(deleted_messages) - 1} messages.\n"

        deleted_messages.pop(0)

        for deleted_message in deleted_messages:
            message += f"\n<@{deleted_message.author.id}>: {deleted_message.content}"

        await ctx.channel.send(message)
    
def setup(bot: Bot):
    bot.add_cog(Delete(bot))