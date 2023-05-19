import discord, os
from dotenv import load_dotenv

class Bot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discord.Message):
        print(f'Message from {message.author}: {message.content}')

if __name__ == "__main__":
    load_dotenv()

    intents = discord.Intents.default()
    intents.message_content = True

    client = Bot(intents=intents)
    client.run(os.getenv('TESTTOKEN'))