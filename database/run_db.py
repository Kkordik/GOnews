import asyncio
from database.Tables.ChatsTable import ChatsTable
from config import config_data
from database.Database import SqliteDatabase, MysqlDatabase, Database


async def run_mysql_db(_loop, host, user, password, name, port) -> MysqlDatabase:
    _db = MysqlDatabase(host, user, password, name, port)
    await _db.make_pool(_loop)
    return _db


def run_db() -> SqliteDatabase:
    _db = SqliteDatabase()
    _db.create_tables()
    return _db


if __name__ == "database.run_db":
    # # Register database and pool (mysql)
    # loop = asyncio.get_event_loop()
    # db: Database = loop.run_until_complete(run_db(loop, config_data['HOST'], config_data['USER'], config_data['PASSWORD'], config_data['NAME'], config_data['PORT']))

    db = run_db()

    # Register main tables
    chat_tb = ChatsTable(db)
