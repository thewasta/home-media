import configparser
import re
from pathlib import Path, PurePath

from telethon.tl.custom import Message

from channels.ChannelFactory import ChannelFactory
from utils.FileMimeType import FileMimeType

config = configparser.ConfigParser()
config.read("config.ini")


class Shingeki(ChannelFactory):
    def __init__(self):
        self.show = "Shingeki No Kyojin"
        self.parent = "Anime"

    def must_ignore(self, message: Message) -> bool:
        pass

    def get_path(self, message: Message):
        if not self.must_ignore(message):
            file_type = FileMimeType.get_mime(message.media.document.mime_type)
            main_folder_path = PurePath(str(config['Telegram']['PATH']), self.parent, "TV", self.show)
            if "OVA" not in message.message:
                is_part = re.search("part", message.message, flags=re.IGNORECASE)
                chapter = 0
                if "The Final Season" in message.message and not is_part:
                    chapter = re.search("(?<=sodio)(.*)(\d){1,2}", message.message).group().replace(" ", "")
                    chapter = 59 + int(chapter)
                if is_part and "The Final Season" in message.message:
                    chapter = re.search("(?<=sodio)(.*)(\d){1,2}", message.message).group().replace(" ", "")
                    chapter = int(chapter) + 75
                if "#" in message.message:
                    chapter = re.search("(?<=#)(.*)(\d){1,2}", message.message).group().replace("Episode_", "")
                file_name = f"{self.show} episode {chapter}.{file_type}"
                abs_path = Path(PurePath(main_folder_path, file_name))
            else:
                main_folder_path = PurePath(str(config['Telegram']['PATH']), self.parent, "Movies", self.show)
                regrex_pattern = re.compile(pattern="["
                                                    u"\U0001F600-\U0001F64F"  # emoticons
                                                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                                    "]+", flags=re.UNICODE)
                remove_emoji = regrex_pattern.sub(r'', re.match("[\s\S]*?(?=_)", message.message).group()).strip()
                file_name = f'{remove_emoji}.{file_type}'.replace("\n", "")

                abs_path = Path(PurePath(main_folder_path, file_name))
            return Path(abs_path)
