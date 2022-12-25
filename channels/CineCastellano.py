import configparser
import re
import string
from pathlib import Path, PurePath
from cleantext import clean
from telethon.tl.custom.message import Message

from channels.ChannelFactory import ChannelFactory
from utils.FileMimeType import FileMimeType

config = configparser.ConfigParser()
config.read("config.ini")


class CineCastellano(ChannelFactory):
    def __init__(self):
        self.parent = "Films"

    def must_ignore(self, message: Message) -> bool:
        pass

    def get_path(self, message: Message) -> Path:
        media_url = None
        file_mime = FileMimeType.get_mime(message.media.document.mime_type)
        remove_emojis = clean(message.message, no_emoji=True)
        pattern = r'[' + string.punctuation + ']'
        remove_special_characters = re.sub(pattern, "", remove_emojis)
        file_name = re.sub("\n(?<=\n)[^\]]+", "", remove_special_characters)

        if message.entities[0].url:
            media_url = message.entities[0].url
        mdb_id = None
        if media_url:
            mdb_id = re.search("tt\d.+?(?=\/)", media_url).group()
        if mdb_id:
            file_name = f"{file_name} [{mdb_id}]"
        main_folder_path = PurePath(str(config['Telegram']['PATH']), self.parent)
        return Path(PurePath(main_folder_path, file_name, f"{file_name}.{file_mime}"))
