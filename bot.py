import discord, os
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
        for sub_dir, _, files in os.walk('./cogs'):
            for filename in files:
                if filename.endswith('.py'):
                    cog_name = os.path.splitext(filename)[0]
                    sub_dir_name = sub_dir.split('/').pop()
                    self.load_extension(f'cogs.{sub_dir_name}.{cog_name}')

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