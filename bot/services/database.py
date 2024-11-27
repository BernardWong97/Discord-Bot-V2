from loguru import logger
from config import DB_CONFIG
from mysql.connector import Error
from mysql.connector.aio import connect

class DatabaseService:
    def __init__(self):
        self.connection = None
        self.last_id = None

    async def connect(self):
        try:
            logger.info('Connecting to database...')
            self.connection = await connect(**DB_CONFIG)

            if await self.connection.is_connected():
                logger.success('Successfully connected to database!')
            else:
                logger.error('Connection to database failed')
        except Error as e:
            logger.error(f"Error connecting to MYSQL database: {e}")

    async def query(self, query: str, params: tuple = None):
        if self.connection is None:
            await self.connect()

        async with await self.connection.cursor() as cursor:
            try:
                await cursor.execute(query, params)
                result = await cursor.fetchall()
                return result
            except Error as e:
                logger.error(f"Error executing query: {e}")

    async def execute(self, query: str, params: tuple = None):
        if self.connection is None:
            await self.connect()

        async with await self.connection.cursor() as cursor:
            try:
                await cursor.execute(query, params)
                await self.connection.commit()
                data = cursor.rowcount
                self.last_id = cursor.lastrowid

                return data
            except Error as e:
                logger.error(f"Error executing query: {e}")

    async def close(self):
        if self.connection and await self.connection.is_connected():
            await self.connection.close()
            logger.success('Connection to database closed')