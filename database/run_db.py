from database.Tables.ChatsTable import ChatsTable
from database.Tables.UrlsTable import UrlsTable
from database.Database import SqliteDatabase


def run_db() -> SqliteDatabase:
    _db = SqliteDatabase()
    _db.create_tables()
    return _db


if __name__ == "database.run_db":
    db = run_db()

    # Register main tables
    chat_tb = ChatsTable(db)
    urls_tb = UrlsTable(db)

