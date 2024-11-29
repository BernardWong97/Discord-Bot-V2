import os
from discord.ext.commands import Bot
from discord import Intents
from bot.services.database import DatabaseService
from bot.services.llm import LLMService
from bot.services.pokedex import PokedexService

class Bot(Bot):
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Bot, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_is_initialized"):
            super().__init__(command_prefix="", intents=Intents.all())
            self._is_initialized = True
            self.database = None
            self.ai = None
            self.pokedex = None
            self.reminders = []

            self.__initialize()

    def __initialize(self):
        self.__load_cogs()
        self.ai = LLMService()
        self.pokedex = PokedexService()
        
    def __load_cogs(self):
        for sub_dir, _, files in os.walk(os.path.join('bot', 'cogs')):
            for filename in files:
                if filename.endswith('.py') and not filename.startswith('_'):
                    cog_name = os.path.splitext(filename)[0]
                    sub_dir_name = sub_dir.split(os.sep).pop()
                    self.load_extension(f'bot.cogs.{sub_dir_name}.{cog_name}')

    async def connect_database(self):
        self.database = DatabaseService()
        await self.database.connect()

    async def init_pokedex(self):
        await self.pokedex.get_all_data()

bot = Bot()