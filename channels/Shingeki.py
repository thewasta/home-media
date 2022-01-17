import configparser
import re
from pathlib import Path, PurePath

from telethon.tl.custom import Message

from channels.ChannelFatory import ChannelFactory
from utils.FileMimeType import FileMimeType

config = configparser.ConfigParser()
config.read("config.ini")


class Shingeki(ChannelFactory):
    def __init__(self):
        self.show = "Shingeki No Kyojin"
        self.parent = "Anime"
        self.file = ""

    def must_ignore(self, message: Message) -> bool:
        pass

    def get_path(self, message: Message):
        if not self.must_ignore(message):
            file_type = FileMimeType.get_mime(message.media.document.mime_type)
            main_folder_path = PurePath(str(config['Telegram']['PATH']), self.parent, "TV", self.show)
            season = message.message.split(" ")[0].replace("T", "S0")
            chapter = re.search("(?<=ulo)(.*)(\d){1,2}", message.message).group().replace(" ", "")
            if "parte" in message.message:
                episode = 75 + int(chapter)
                file_name = f"{self.show} episode {episode}.{file_type}"
            elif "4" in season and "parte" not in message.message:
                episode = 59 + int(chapter)
                file_name = f"{self.show} episode {episode}.{file_type}"
            elif "3" in season:
                episode = 37 + int(chapter)
                file_name = f"{self.show} episode {episode}.{file_type}"
            elif "2" in season:
                episode = 26 + int(chapter)
                file_name = f"{self.show} episode {episode}.{file_type}"
            else:
                file_name = f"{self.show} episode {chapter}.{file_type}"
            abs_path = Path(PurePath(main_folder_path, file_name))
            return Path(abs_path)
