from telethon.sync import TelegramClient
import re
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def get_chats():
    client = TelegramClient('dialog-session', int(config['Telegram']['API_TOKEN']), str(config['Telegram']['API_HASH']))

    client.start()

    chats = []
    for dialog in client.iter_dialogs():
        chats.append({
            "name": re.sub("[^\w ]", "", dialog.name),
            "id": str(dialog.id)
        })

    client.disconnect()
    return chats


def get_chat_id(chat_name):
    client = TelegramClient('session', int(config['Telegram']['API_TOKEN']), str(config['Telegram']['API_HASH']))

    client.start()
    entity = client.get_entity(1171137336)
    chat_id = entity.id
    print(chat_id, entity.title)
    client.disconnect()
    return chat_id


print(get_chat_id(""))
