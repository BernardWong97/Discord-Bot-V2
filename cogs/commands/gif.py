import discord, os, requests, random
import urllib.parse
from discord import Option, ApplicationContext
from discord.ext.commands import Bot, Cog

class Gif(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @discord.slash_command(name="gif", description="Generate a random gif", guild_ids=[int(os.getenv('GUILD'))])
    async def gif(self, ctx: ApplicationContext, keyword: Option(str, description="The keyword of the gif", default="chicken")):
        keyword = urllib.parse.quote(keyword)
        url = f"https://g.tenor.com/v1/search?q={keyword}&key={os.getenv('TENOR_KEY')}&limit=10"

        response = requests.get(url)
        json = response.json()
        index = random.randint(0, len(json['results']) - 1)

        await ctx.respond(json['results'][index]['url'])

def setup(bot: Bot):
    bot.add_cog(Gif(bot))