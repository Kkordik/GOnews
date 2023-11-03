import typing
from database.Database import Database
from database.Tables.Table import SqliteTable
from datetime import datetime


class UrlsTable(SqliteTable):
    """
    chat_id	bigint
    delete_tails	text
    """
    __name = "chats"
    __columns = ["id", "url", "date_added"]

    def __init__(self, db: Database):
        super().__init__(self.__name, db, self.__columns)


class UrlsDb:
    def __init__(self, table: UrlsTable, id: int = None, url: str = None, date_added: datetime = None):
        self.table: UrlsTable = table
        self.id: int = id
        self.url: str = url
        self.date_added: datetime = date_added

    def add_url(self, url=None):
        self.url = url or self.url

        if not self.url:
            raise Exception("No url specified to add_url")

        return self.table.insert_vals(url=self.url)

    def del_url(self, url=None, id=None):
        self.url = url or self.url
        self.id = id or self.id

        if self.url is None and self.id is None:
            raise Exception("No url/id specified to del_url")
        elif self.url:
            return self.table.delete_line(url=self.url)
        else:
            return self.table.delete_line(id=self.id)

    def get_all_urls(self):
        return self.table.select_vals()
