import asyncio
from database.Tables.ChatTable import ChatTable
from config import HOST, USER, PASSWORD, NAME, PORT
from database.Database import SqliteDatabase, MysqlDatabase, Database


async def run_mysql_db(_loop, host, user, password, name, port) -> MysqlDatabase:
    _db = MysqlDatabase(host, user, password, name, port)
    await _db.make_pool(_loop)
    return _db


def run_db() -> SqliteDatabase:
    return SqliteDatabase()


if __name__ == "database.run_db":
    # # Register database and pool (mysql)
    # loop = asyncio.get_event_loop()
    # db: Database = loop.run_until_complete(run_db(loop, HOST, USER, PASSWORD, NAME, PORT))

    db = run_db()

    # Register main tables
    chat_tb = ChatTable(db)
