import typing
from database.Database import Database
from database.Tables.Table import SqliteTable
from datetime import datetime


class ChatsTable(SqliteTable):
    """
    chat_id	bigint
    delete_tails	text
    """
    __name = "chats"
    __columns = ["chat_id", "delete_tails", "date_added"]

    def __init__(self, db: Database):
        super().__init__(self.__name, db, self.__columns)


class ChatDb:
    def __init__(self, table: ChatsTable, chat_id, is_parsed: bool = None, delete_tails: typing.List[str] = None,
                 date_added: datetime = None):
        self.table: ChatsTable = table
        self.chat_id: int = int(chat_id)
        self.is_parsed: bool = is_parsed
        self.delete_tails: typing.List[str] = delete_tails
        self.date_added: datetime = date_added

    def check_is_parsed(self, chat_id=None) -> bool:
        if chat_id:
            self.chat_id = chat_id
        elif not self.chat_id:
            raise Exception("No chat_id specified to get it by id")

        res = self.table.select_vals(chat_id=self.chat_id)

        self.is_parsed = bool(res)

        return self.is_parsed

    def add_chat(self, delete_tails: str, chat_id=None):
        if chat_id:
            self.chat_id = chat_id
        elif not self.chat_id:
            raise Exception("No chat_id specified to add_chat")

        return self.table.insert_vals(chat_id=self.chat_id, delete_tails=delete_tails)

    def get_delete_tails(self, chat_id=None):
        if chat_id:
            self.chat_id = chat_id
        elif not self.chat_id:
            raise Exception("No chat_id specified to get_delete_tails")

        res = self.table.select_vals(chat_id=self.chat_id)

        if not res:
            raise Exception("This chat is not in the database")

        self.delete_tails = res[0]['delete_tails'].split(',') if res[0]['delete_tails'] else []

        return self.delete_tails

