import discord, os
from discord import Option, ApplicationContext
from discord.ext.commands import Bot, Cog

class Send(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @discord.slash_command(name="send", description="Send message", guild_ids=[int(os.getenv('TEST_GUILD'))])
    async def gif(self, ctx: ApplicationContext, message: Option(str, description="The message to be send"), channel: Option(discord.TextChannel, description="Choose a channel")):
        await ctx.defer(ephemeral=True)
        await channel.send(message)
        await ctx.followup.send(f'`{message}` has been sent to **[#{channel.name}](<https://discord.com/channels/{ctx.guild.id}/{channel.id}>)**', wait=True)
    
def setup(bot: Bot):
    bot.add_cog(Send(bot))