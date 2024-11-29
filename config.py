import os
from datetime import timezone, timedelta
from loguru import logger
from dotenv import load_dotenv
    
logger.info('Loading environmental variables...')
if load_dotenv(override=True):
    logger.success('Environmental variables loaded!')
else:
    logger.error('Environmental variables not loaded')

TIMEZONE = timezone(timedelta(hours=8), name='Asia/Kuala_Lumpur')

TOKEN = os.getenv('TOKEN')
BOT_ID = int(os.getenv('TEST_BOT_ID'))
GUILD = int(os.getenv('TEST_GUILD'))
ALL_CHAT_CHANNEL = int(os.getenv('TEST_CHANNEL'))

GIF_KEY = os.getenv('TENOR_KEY')

DB_CONFIG = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PW'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DB'),
    'port': int(os.getenv('MYSQL_PORT'))
}

REMINDER_TABLE = os.getenv('MYSQL_REMINDER_TABLE')
MEMBER_TABLE = os.getenv('MYSQL_MEMBER_TABLE')
QUOTE_TABLE = os.getenv('MYSQL_QUOTE_TABLE')

OWNER_ID = int(os.getenv('BERD_ID'))