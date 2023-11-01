import asyncio
from database.Tables.ChatsTable import ChatsTable
from config import config_data
from database.Database import SqliteDatabase, Database



def run_db() -> SqliteDatabase:
    _db = SqliteDatabase()
    _db.create_tables()
    return _db


if __name__ == "database.run_db":
    db = run_db()

    # Register main tables
    chat_tb = ChatsTable(db)
