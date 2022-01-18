import configparser
from pathlib import PurePath, Path

from telethon.tl.custom import Message

from channels.ChannelFactory import ChannelFactory

config = configparser.ConfigParser()
config.read("config.ini")


class SouthPark(ChannelFactory):
    def __init__(self):
        self.show = "South Park"
        self.parent = "TV Shows"

    def must_ignore(self, message: Message) -> bool:
        pass

    # noinspection PyMethodMayBeStatic
    def __has_attribute(self, message: Message) -> bool:
        return hasattr(message.media.document.attributes[0], "file_name")

    def get_path(self, message: Message):
        if not self.must_ignore(message) and self.__has_attribute(message):
            main_folder_path = PurePath(str(config['Telegram']['PATH']), self.parent, self.show)
            file_name = message.media.document.attributes[0].file_name
            abs_path = Path(PurePath(main_folder_path, file_name))
            return Path(abs_path)
