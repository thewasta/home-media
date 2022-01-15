from channels.ChannelFatory import ChannelFactory
from pathlib import Path
from telethon.tl.custom.message import Message
from telethon import TelegramClient
from utils.FileMimeType import FileMimeType


class OnePiece(ChannelFactory):
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.show = "One Piece"

    def make_directory(self, abs_path: Path):
        ""

    async def download_file(self, client: TelegramClient, message: Message, abs_path):
        if not self.already_downloaded(message) and not self.should_ignore(message):
            file_type = FileMimeType.get_mime(message.media.document.mime_type)
            if "#" in message.message:
                print(message.message)
                self.start_download(message)
                self.download_finished(message)

    def should_ignore(self, message) -> bool:
        """"""
