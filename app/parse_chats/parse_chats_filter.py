from pyrogram import filters
from database.Tables.ChatsTable import ChatDb
from database.run_db import chat_tb


async def check_is_parsed(_, __, message):
    chat_db = ChatDb(table=chat_tb, chat_id=message.chat.id)
    return chat_db.check_is_parsed()

filter_parsed_chat = filters.create(check_is_parsed)
