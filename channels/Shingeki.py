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
            chapter = "0" + chapter if int(chapter) < 10 else chapter
            if "parte" in message.message:
                file_name = f"{self.show} {season}E{chapter}- part 2.{file_type}"
            else:
                file_name = f"{self.show} - {season}E{chapter}.{file_type}"
            abs_path = Path(PurePath(main_folder_path, file_name))
            return Path(abs_path)
