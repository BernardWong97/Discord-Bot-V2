import os
from discord import Intents
from discord.ext.commands import Bot
from dotenv import load_dotenv

class Bot(Bot):
    def __init__(self):
        super().__init__(command_prefix="", intents=Intents.all())
        self.load_cogs()

    def load_cogs(self):
        for sub_dir, _, files in os.walk(os.path.join('.', 'cogs')):
            for filename in files:
                if filename.endswith('.py'):
                    cog_name = os.path.splitext(filename)[0]
                    sub_dir_name = sub_dir.split(os.sep).pop()
                    self.load_extension(f'cogs.{sub_dir_name}.{cog_name}')

if __name__ == '__main__':
    # Load environmental variables
    load_dotenv()

    # Instantiate
    print('Initiating Bot')
    bot = Bot()

    # Login
    bot.run(os.getenv('TEST_TOKEN'))