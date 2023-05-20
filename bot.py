import discord, os, asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="", intents=discord.Intents.all())

    async def on_ready(self):
        print(f'Logged in as {self.user}!')
        print(f'{self.user.name} is listening for Discord Messages!')

    async def on_member_join(self, member: discord.Member):
        print(f'Hello {member.name}')

    async def load_cogs(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')

async def main():
    # Load environmental variables
    load_dotenv()

    # Instantiate
    print('Initiating Bot')
    bot = Bot()

    async with bot:
        # Load cogs
        await bot.load_cogs()

        # Login
        await bot.start(os.getenv('TEST_TOKEN'))

asyncio.run(main())