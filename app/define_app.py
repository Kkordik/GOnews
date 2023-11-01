from pyrogram import Client, enums
from config import config_data

app = Client("my_account", config_data['essential']['API_ID'], config_data['essential']['API_HASH'],
             parse_mode=enums.ParseMode.HTML)
