import discord, os, asyncio
from discord.ext import commands
from discord.ext.commands.context import Context
from dotenv import load_dotenv

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="", intents=discord.Intents.all())

    async def on_ready(self):
        print(f'Logged in as {self.user}!')
        print(f'{self.user.name} is listening for Discord Messages!')

    async def on_member_join(self, member: discord.Member):
        print(f'Hello {member.name}')

    async def on_command_error(self, context: Context, exception: discord.DiscordException):
        if isinstance(exception, commands.CommandNotFound):
            return
        
        return await super().on_command_error(context, exception)

    def load_cogs(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    # Load environmental variables
    load_dotenv()

    # Instantiate
    print('Initiating Bot')
    bot = Bot()

    # Load cogs
    bot.load_cogs()

    # Login
    bot.run(os.getenv('TEST_TOKEN'))