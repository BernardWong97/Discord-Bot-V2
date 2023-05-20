import discord, os
from discord import Option
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context

class Send(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @discord.slash_command(name="send", description="Send message", guild_ids=[int(os.getenv('TEST_GUILD'))])
    async def gif(self, ctx: Context, message: Option(str, description="The message to be send"), channel: Option(discord.TextChannel, description="Choose a channel")):
        await ctx.defer(ephemeral=True)
        await channel.send(message)
        await ctx.followup.send(f'`{message}` has been sent to **#{channel.name}**')

def setup(bot: Bot):
    bot.add_cog(Send(bot))