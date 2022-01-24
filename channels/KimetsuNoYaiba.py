import configparser
import re
from pathlib import PurePath, Path

from telethon.tl.custom import Message

from channels.ChannelFactory import ChannelFactory
from utils.FileMimeType import FileMimeType

config = configparser.ConfigParser()
config.read("config.ini")


class KimetsuNoYaiba(ChannelFactory):
    def __init__(self):
        self.show = "Kimetsu No Yaiba"
        self.parent = "Anime"
        self.quality = {
            "full": 1080,
            "hd": 720
        }

    def must_ignore(self, message: Message) -> bool:
        if re.search("movie", message.message, flags=re.IGNORECASE) and \
                re.search("latino", message.message, flags=re.IGNORECASE) is None:
            return False
        if hasattr(message.media.document.attributes[0], "duration") and \
                message.media.document.attributes[0].duration < 1100:
            return True
        if re.search("memes", message.message, flags=re.IGNORECASE) is not None:
            return True
        if re.search("capitulo", message.message, flags=re.IGNORECASE) is None and \
                re.search("episodio", message.message, flags=re.IGNORECASE) is None:
            return True
        return re.search("latino", message.message, flags=re.IGNORECASE) is not None

    def get_path(self, message: Message):
        ignore = self.must_ignore(message)
        if not ignore:
            file_type = FileMimeType.get_mime(message.media.document.mime_type)
            main_folder_path = PurePath(str(config['Telegram']['PATH']), self.parent, "TV", self.show)

            remove_hashtag = self.remove_hashtag(message)
            if re.search("movie", message.message, flags=re.IGNORECASE) is None:
                chapter = re.search("\d{1,2}", message.message).group()
                quality = self.get_video_quality(message)
                if re.search("Yuukaku", remove_hashtag, flags=re.IGNORECASE):
                    season = 3
                elif re.search("Mugen", message.message, flags=re.IGNORECASE):
                    season = 2
                else:
                    season = 1
                file_name = f"{self.show} S0{season}E{chapter} - {quality}p.{file_type}"
            else:
                main_folder_path = PurePath(str(config['Telegram']['PATH']), self.parent, "Movies", self.show)
                file_name = f"{self.show} Mugen Ressha Hen [tvdbid=131963].{file_type}"
            return Path(PurePath(main_folder_path, file_name))

    # noinspection PyMethodMayBeStatic
    def remove_hashtag(self, message: Message):
        return re.sub("(?<=#)[\s\S]*", "", message.message, flags=re.IGNORECASE).replace("#", "").strip()

    # noinspection PyMethodMayBeStatic
    def get_video_quality(self, message: Message) -> str:
        m = message.message
        quality = "720"
        if "full" in m or "1080" in m:
            quality = "1080"
        if "360" in m:
            quality = "360"
        if "480" in m:
            quality = "480"
        return quality
