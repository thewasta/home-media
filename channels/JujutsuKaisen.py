import configparser
import re
from pathlib import Path, PurePath

from telethon.tl.custom.message import Message

from channels.ChannelFactory import ChannelFactory
from utils.FileMimeType import FileMimeType

config = configparser.ConfigParser()
config.read("config.ini")


class JujutsuKaisen(ChannelFactory):
    def __init__(self):
        self.show = "Jujutsu Kaisen"
        self.parent = "Anime"

    def must_ignore(self, message: Message) -> bool:
        pass

    def get_path(self, message: Message) -> Path:
        if not self.must_ignore(message):
            file_type = FileMimeType.get_mime(message.media.document.mime_type)
            main_folder_path = PurePath(str(config['Telegram']['PATH']), self.parent, "TV", self.show)
            if not self.must_ignore(message):
                search_chapter = re.search("(\d){1,3}", message.message)
                if search_chapter is not None:
                    chapter = int(search_chapter.group())
                    file_name = f"{self.show} episode {chapter}.{file_type}"
                    return Path(PurePath(main_folder_path, file_name))
