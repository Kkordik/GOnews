from app.parse_admin_chat.parse_admin_chat_filter import filter_admin_chat
from app.define_app import app
from database.Tables.ChatsTable import ChatDb
from database.run_db import chat_tb


@app.on_message(filter_admin_chat)
async def hello(_, message):
    if not message.text:
        return
    # !send <to_chat_id> <from_chat_id> <message_id>
    if '!send' in message.text:
        # Getting information from the command
        try:
            to_chat_id = message.text.split()[1]
            from_chat_id = message.text.split()[2]
            message_id = int(message.text.split()[3])

            message = await app.get_messages(chat_id=from_chat_id, message_ids=message_id)
            text = message.text or message.caption
            text = text.html if text else None
        except Exception as ex:
            await app.send_message(chat_id=message.chat.id,
                                   text=f'Проверь правильность комманды, ошибка:\n\n{ex}')
            return

        if not message.media_group_id:
            # Sending an edited post to the channel, not a group of media
            await app.copy_message(chat_id=to_chat_id,
                                   from_chat_id=from_chat_id,
                                   message_id=message_id,
                                   caption=text)
        else:
            await app.copy_media_group(chat_id=to_chat_id,
                                       from_chat_id=from_chat_id,
                                       message_id=message_id,
                                       captions=text)

    # !channel <username> '<tails divided by comma without space>'
    elif '!channel' in message.text:
        # Getting information from the command
        try:
            channel_username = message.text.split()[1]
            # Adding '@' to the username, if it wasn't
            if '@' not in channel_username and '/' not in channel_username:
                channel_username = '@' + channel_username
            elif 't.me/' in channel_username and '/+' not in channel_username:
                channel_username = '@' + channel_username.split('t.me/')[1]
            channel_delete_tails = message.text.split("'")[1] if len(message.text.split("'")[1]) > 0 else None
        except Exception as ex:
            await app.send_message(chat_id=message.chat.id,
                                   text=f'Проверь правильность комманды, ошибка:\n\n{ex}')
            return
        print(channel_username)
        try:
            channel_chat = await app.join_chat(chat_id=channel_username)
        except Exception as ex:
            if 'USER_ALREADY_PARTICIPANT' not in str(ex):
                await app.send_message(chat_id=message.chat.id,
                                       text=f'Канал не найден или не удалось подписаться, ошибка:\n\n{ex}')
                return
            else:
                channel_chat = await app.get_chat(chat_id=channel_username)

        # Adding channel to the database
        chat_db = ChatDb(table=chat_tb, chat_id=channel_chat.id)
        chat_db.add_chat(delete_tails=channel_delete_tails)

        await app.send_message(chat_id=message.chat.id, text='Готово! Канал добавлен.')
