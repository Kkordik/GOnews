import sqlite3
from datetime import datetime


def convert_timestamp(ts):
    return datetime.strptime(ts.decode('utf-8'), "%Y-%m-%d %H:%M:%S")


def adapt_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("timestamp", convert_timestamp)


class Database:
    def execute_db(self, *args, **kwargs):
        pass


class SqliteDatabase(Database):
    def create_tables(self):
        self.execute_db("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id BIGINT NOT NULL PRIMARY KEY,
            delete_tails TEXT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.execute_db("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url VARCHAR(2048) NOT NULL UNIQUE,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)

    @staticmethod
    def execute_db(command: str, values: list = None):
        """
        Execute any given command and return fetchall

        :param command: Sqlite executable command
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
