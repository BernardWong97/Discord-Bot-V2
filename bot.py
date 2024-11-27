from loguru import logger
from bot.bot_instance import bot
from config import TOKEN

if __name__ == '__main__':
    logger.info('Initiating bot...')
    bot.run(TOKEN)