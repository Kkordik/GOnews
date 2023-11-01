import aiomysql
from aiomysql import Pool
import sqlite3


class Database:
    def execute_db(self, *args, **kwargs):
        pass


class MysqlDatabase(Database):
    def __init__(self, host: str, user: str, password: str,  name: str, pool: Pool = None, port: int = 3306):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__port = port

        self.__name = name
        self.__pool: Pool = pool

    async def make_pool(self, loop):
        self.__pool = await aiomysql.create_pool(host=self.__host, port=self.__port, user=self.__user,
                                                 password=self.__password, db=self.__name, autocommit=False, loop=loop)
        return self.__pool

    async def execute_db(self, command: str, values: list = None):
        """
        Execute any given command and return fetchall

        :param command: MySQL executable command
        :param values: Values to replace %s
        :return: list of fetched rows
        """
        async with self.__pool.acquire() as con:
            async with con.cursor() as cur:
                await cur.execute(command, values)
                res = await cur.fetchall()
            await con.commit()
        return res


class SqliteDatabase(Database):
    def create_tables(self):
        self.execute_db("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id BIGINT NOT NULL PRIMARY KEY,
            delete_tails TEXT
        );
        """)

    @staticmethod
    def execute_db(command: str, values: list = None):
        """
        Execute any given command and return fetchall

        :param command: MySQL executable command
        :param values: Values to replace %s
        :return: list of fetched rows
        """
        with sqlite3.connect("bot_sqlite.db") as con:
            cur = con.cursor()
            if values is not None:
                values = tuple(values)
                cur.execute(command, values)
            else:
                cur.execute(command)
            res = cur.fetchall()
            con.commit()
        return res
