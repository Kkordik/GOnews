from pyrogram import filters
from config import ADMIN_CHAT_ID


async def check_admin_chat(_, __, message):
    return int(message.chat.id) == ADMIN_CHAT_ID

filter_admin_chat = filters.create(check_admin_chat)
