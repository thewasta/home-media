from channels.ChannelFatory import ChannelFactory
from pathlib import Path, PurePath
from telethon.tl.custom.message import Message
from utils.FileMimeType import FileMimeType
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class OnePiece(ChannelFactory):
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.show = "One Piece"
        self.parent = "Anime"
        self.file = ""

    def must_ignore(self, message) -> bool:
        return "3D" in message.message or "Película" in message.message

    def get_path(self, message: Message):
        file_type = FileMimeType.get_mime(message.media.document.mime_type)
        main_folder_path = PurePath(str(config['Telegram']['PATH']), self.parent, "TV", self.show)
        if "Cap" in message.message:
            chapter = message.message.split(" ")[0]
            chapter = chapter.replace("#", "")
            chapter = chapter.replace("Cap", "")
            file_name = f"One Piece S01E{chapter}.{file_type}"
            abs_path = Path(PurePath(main_folder_path, file_name))
            return Path(abs_path)
