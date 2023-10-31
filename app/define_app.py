from pyrogram import Client, enums
from config import api_id, api_hash

app = Client("my_account", api_id, api_hash,
             parse_mode=enums.ParseMode.HTML)
