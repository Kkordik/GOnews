import sqlite3


class Database:
    def execute_db(self, *args, **kwargs):
        pass


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
