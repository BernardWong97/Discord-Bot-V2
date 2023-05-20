import discord, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from discord import Embed
from discord.ext.commands import Bot, Cog, Context

class NukeCodes(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @discord.slash_command(name="nuke_codes", description="Retrieve this weeks's Fallout 76 nuke codes", guild_ids=[int(os.getenv('TEST_GUILD'))])
    async def gif(self, ctx: Context):
        await ctx.defer()

        target_url = "https://nukacrypt.com"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True

        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) as driver:
            driver.get(target_url)

            embed_message = Embed(title="Nuclear codes",
                            colour=0xFF00FF,
                            url=target_url,
                            description="Nukes Codes in [Fallout 76](https://www.falloutbuilds.com/fo76/) are weekly changing codes to launch nuclear missiles.\n\nNuke Codes always have 8 digits and are only valid in their corresponding nuclear silo: Alpha, Bravo, and Charlie. You can use the launch control terminal in any of these silos to specify a location on the [Fallout 76 Map](https://www.falloutbuilds.com/fo76/map/) as a target for your nuclear missile."
                        )

            embed_message.set_thumbnail(url='https://s3.amazonaws.com/esohelpportal/Fallout+Icons+for+KB+Articles/Nuke.png')

            embed_message.add_field(name='\u200B', value='\u200B', inline=False)

            element = driver.find_element(By.XPATH, '//div[@id="content"]/div/div[1]')

            data = element.text.strip().split("\n")

            data.pop()

            for i in range(0, len(data), 2):
                title = data[i]
                code = data[i + 1]

                embed_message.add_field(name=f"__{title}__", value=f"**{code}**", inline=True)

            message = await ctx.followup.send(embed=embed_message)

            pins = await ctx.channel.pins()

            for pin in pins:
                if pin.author.bot:
                    await pin.unpin()

            await message.pin()

def setup(bot: Bot):
    bot.add_cog(NukeCodes(bot))