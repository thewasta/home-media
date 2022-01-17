import re
from pathlib import Path, PurePath
from telethon.tl.custom import Message
from utils.FileMimeType import FileMimeType

from channels.ChannelFatory import ChannelFactory
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class YoungSheldon(ChannelFactory):
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.show = "Young Sheldon {tvdb-328724}"
        self.parent = "TV Shows"
        self.file = ""

    def must_ignore(self, message: Message) -> bool:
        """"""

    def get_path(self, message: Message):
        dialog_message = message.message
        file_type = FileMimeType.get_mime(message.media.document.mime_type)
        main_folder_path = PurePath(str(config['Telegram']['PATH']), self.parent, self.show)
        if re.findall('cap|episodio', dialog_message, flags=re.IGNORECASE):
            chapter = re.findall("\d{1,2}", dialog_message)[0]
            if re.search("^Temporada", dialog_message):
                season = re.findall("\d{1,2}", dialog_message)[0]
                chapter = re.findall("\d{1,2}", dialog_message)[1]
                file_name = f"Young Sheldon S0{season}E{chapter}.{file_type}"
            else:
                file_name = f"Young Sheldon S01E{chapter}.{file_type}"
            abs_path = Path(PurePath(main_folder_path, file_name))
            return Path(abs_path)
