import configparser
import re

from pathlib import Path, PurePath

from telethon.tl.custom import Message
from utils.FileMimeType import FileMimeType

from channels.ChannelFactory import ChannelFactory

config = configparser.ConfigParser()
config.read("config.ini")


class Friends(ChannelFactory):
    def __init__(self):
        self.show = "Friends"
        self.parent = "TV Shows"

    def must_ignore(self, message: Message) -> bool:
        file_name = message.media.document.attributes[0].file_name
        season = re.search("S\d{2}", file_name).group()
        if "S05" in season:
            print("false", season)
            return True
        pass

    def get_path(self, message: Message):
        main_folder_path = PurePath(str(config['Telegram']['PATH']), self.parent, self.show)
        if not self.must_ignore(message):
            message_media_name = message.media.document.attributes[0].file_name
            file_mime = FileMimeType.get_mime(message.media.document.mime_type)
            chapter = re.search("E\d{2}", message_media_name).group()
            season = re.search("S\d{2}", message_media_name).group()

            file_name = f"{self.show} {season}{chapter}.{file_mime}"
            return Path(PurePath(main_folder_path, f"Season {int(season[-2:])}", file_name))
