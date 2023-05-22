import os
from discord import DiscordException, Member, Intents
from discord.ext.commands import Bot, CommandNotFound
from discord.ext.commands.context import Context
from dotenv import load_dotenv
from utilities.members import fetch_members

class Bot(Bot):
    def __init__(self):
        super().__init__(command_prefix="", intents=Intents.all())
        self.load_cogs()

    async def on_ready(self):
        print(f'Logged in as {self.user}!')
        print(f'{self.user.name} is listening for Discord Messages!')

        await fetch_members(self)

    async def on_member_join(self, member: Member):
        await fetch_members(self)
        print(f'Hello {member.name}')

    async def on_command_error(self, context: Context, exception: DiscordException):
        if isinstance(exception, CommandNotFound):
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

    # Login
    bot.run(os.getenv('TEST_TOKEN'))