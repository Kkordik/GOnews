from app.parse_chats.parse_chats_filter import filter_parsed_chat
from app.define_app import app
from database.Tables.ChatsTable import ChatDb
from database.run_db import chat_tb
from config import config_data
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.PostText import PostText


def edited_post_keyboard(to_chat_id, from_chat_id, message_id):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Отправить в канал', callback_data=f'send {to_chat_id}.{from_chat_id}.{message_id}')]
    ])
    return keyboard


def translated_post_keyboard(to_chat_id, from_chat_id, message_id, orig_message_id):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Отправить в канал', callback_data=f'send {to_chat_id}.{from_chat_id}.{message_id}')],
        [InlineKeyboardButton(text='Перевести заново', callback_data=f'remake {orig_message_id}')]
    ])
    return keyboard


@app.on_message(filter_parsed_chat)
async def hello(_, message):
    orig_text = message.text or message.caption

    # Defining PostText object to edit post text
    post_text = PostText(text=orig_text.html if orig_text else '')

    # Getting delete_tails from db
    chat_db = ChatDb(table=chat_tb, chat_id=message.chat.id)
    chat_db.get_delete_tails()

    # Removing delete_tails and empty html tags from post_text and defining post_text_en
    post_text.remove_patterns(chat_db.delete_tails)
    post_text.remove_empty_tags()

    # Translating the text on ru and adding ending
    if config_data['additional']['USE_GPT']:
        post_text = await post_text.translate(language=config_data['additional']['LANGUAGE'])
    post_text.process_first_paragraph(st_char=config_data['additional']['START_CHAR'],
                                      end_char=config_data['additional']['END_CHAR'])
    post_text.add_new_paragraph(config_data['additional']['ENDING'])

    # If message is a simple text
    if message.text:
        msg = await app.send_message(chat_id=config_data['essential']['ADMIN_CHAT_ID'],
                                     text=post_text.text,
                                     disable_web_page_preview=True)
    # If message is not a simple text and doesn't have 2+ medias
    elif not message.media_group_id:
        msg = await app.copy_message(chat_id=config_data['essential']['ADMIN_CHAT_ID'],
                                     from_chat_id=message.chat.id,
                                     message_id=message.id,
                                     caption=post_text.text)
    # If message has 2+ medias
    elif message.media_group_id:
        media_group_list = await app.get_media_group(chat_id=message.chat.id, message_id=message.id)

        if message.id == media_group_list[0].id:
            msgs = await app.copy_media_group(chat_id=config_data['essential']['ADMIN_CHAT_ID'],
                                              from_chat_id=message.chat.id,
                                              message_id=message.id,
                                              captions=post_text.text)
            msg = msgs[0]
        else:
            return

    else:
        return

    full_chat_obj = await app.get_chat(message.chat.id)
    await app.send_message(chat_id=config_data['essential']['ADMIN_CHAT_ID'],
                           text=f'From channel <a href="{full_chat_obj.invite_link}">{full_chat_obj.title}</a>\n'
                                f'<b>Send this command to copy the post to our channel</b>:'
                                f'\n<code>!send {config_data["essential"]["CHANNEL_ID"]} {config_data["essential"]["ADMIN_CHAT_ID"]} {msg.id}</code> ',
                           disable_web_page_preview=True)
