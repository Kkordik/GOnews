from pyrogram import filters
from config import config_data


async def check_admin_chat(_, __, message):
    return int(message.chat.id) == config_data['essential']['ADMIN_CHAT_ID']

filter_admin_chat = filters.create(check_admin_chat)
