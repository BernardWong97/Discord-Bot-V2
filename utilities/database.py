import mysql.connector, os
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

db_config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PW'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DB')
}

async def retrieve_data(query: str):
    try:
        with mysql.connector.connect(**db_config) as conn:
            # print('Connected to MYSQL database')

            with conn.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()

                return data
    except Error as e:
            raise ValueError(f"Error executing query: {e}")

async def commit_query(query: str, value: tuple):
    try:
        with mysql.connector.connect(**db_config) as conn:
            # print('Connected to MYSQL database')

            with conn.cursor() as cursor:
                cursor.execute(query, value)
                conn.commit()
                data = cursor.rowcount

            return data
    except Error as e:
            raise ValueError(f"Error executing query: {e}")