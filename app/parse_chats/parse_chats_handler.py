from app.parse_chats.parse_chats_filter import filter_parsed_chat
from app.define_app import app
from database.Tables.ChatTable import ChatDb
from database.run_db import chat_tb
from config import ADMIN_CHAT_ID, CHANNEL_ID, EN_CHANNEL_ID, ENDING_RU, ENDING_EN
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
    post_text_ru = PostText(text=orig_text.html if orig_text else '')

    # Getting delete_tails from db
    chat_db = ChatDb(table=chat_tb, chat_id=message.chat.id)
    chat_db.get_delete_tails()

    # Removing delete_tails and empty html tags from post_text_ru and defining post_text_en
    post_text_ru.remove_patterns(chat_db.delete_tails)
    post_text_ru.remove_empty_tags()
    print("text: :: : : : ", post_text_ru.text)
    post_text_en = PostText(post_text_ru.text)

    # Translating the text on ru and adding ending
    await post_text_ru.translate_on_ru()
    post_text_ru.process_first_paragraph()
    post_text_ru.add_new_paragraph(ENDING_RU)

    # If message is a simple text
    if message.text:
        msg = await app.send_message(chat_id=ADMIN_CHAT_ID,
                                     text=post_text_ru.text,
                                     disable_web_page_preview=True)
    # If message is not a simple text and doesn't have 2+ medias
    elif not message.media_group_id:
        msg = await app.copy_message(chat_id=ADMIN_CHAT_ID,
                                     from_chat_id=message.chat.id,
                                     message_id=message.id,
                                     caption=post_text_ru.text)
    # If message has 2+ medias
    elif message.media_group_id:
        media_group_list = await app.get_media_group(chat_id=message.chat.id, message_id=message.id)

        if message.id == media_group_list[0].id:
            msgs = await app.copy_media_group(chat_id=ADMIN_CHAT_ID,
                                              from_chat_id=message.chat.id,
                                              message_id=message.id,
                                              captions=post_text_ru.text)
            msg = msgs[0]
        else:
            return

    else:
        return

    await app.send_message(chat_id=ADMIN_CHAT_ID,
                           text=f'From channel @{message.chat.username}, <b>to send the post to our channel</b>:'
                                f'\n<code>!send {CHANNEL_ID} {ADMIN_CHAT_ID} {msg.id}</code> ')

    # Translating the text on EN and adding ending
    await post_text_en.translate_on_en()
    post_text_en.process_first_paragraph()
    post_text_en.add_new_paragraph(ENDING_EN)

    # If message is a simple text
    if message.text:
        msg = await app.send_message(chat_id=ADMIN_CHAT_ID,
                                     text=post_text_en.text,
                                     disable_web_page_preview=True)
    # If message is not a simple text and doesn't have 2+ medias
    elif not message.media_group_id:
        msg = await app.copy_message(chat_id=ADMIN_CHAT_ID,
                                     from_chat_id=message.chat.id,
                                     message_id=message.id,
                                     caption=post_text_en.text)
    # If message has 2+ medias
    elif message.media_group_id:
        media_group_list = await app.get_media_group(chat_id=message.chat.id, message_id=message.id)

        if message.id == media_group_list[0].id:
            msgs = await app.copy_media_group(chat_id=ADMIN_CHAT_ID,
                                              from_chat_id=message.chat.id,
                                              message_id=message.id,
                                              captions=post_text_en.text)
            msg = msgs[0]
        else:
            return

    else:
        return

    await app.send_message(chat_id=ADMIN_CHAT_ID,
                           text=f'From channel @{message.chat.username}, <b>to send the post to our channel</b>:'
                                f'\n<code>!send {EN_CHANNEL_ID} {ADMIN_CHAT_ID} {msg.id}</code> ')
