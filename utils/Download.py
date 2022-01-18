import configparser
import os
from pathlib import Path

from telethon import TelegramClient
from telethon.tl.custom.message import Message

from utils import bytes_to
from utils import logger
from utils.MetadataDownload import MetadataDownload

config = configparser.ConfigParser()
config.read("config.ini")


def make_directory(abs_path: Path):
    abs_path.parent.mkdir(parents=True, exist_ok=True)


class Download(MetadataDownload):
    def __init__(self):
        self.file = ""

    def progress(self, current, total):
        current_m = bytes_to(current, "m")
        total_b = bytes_to(total, "m")
        path = "/".join(str(self.file).split("/")[-3:])
        logger.info("Download total: {}% {} mb/{} mb {}"
                    .format(int((current / total) * 100), current_m, total_b, path))

    async def download_file(self, client: TelegramClient, message: Message, abs_path=None):
        if not self.already_downloaded(message):
            if abs_path:
                make_directory(abs_path)
                try:
                    offset = os.path.getsize(abs_path)
                except OSError:
                    offset = 0
                with open(abs_path, "ab") as out:
                    self.start_download(message)
                    self.file = abs_path
                    logger.info(f"Inicio de descarga de archivo: {abs_path}")
                    async for chunk in client.iter_download(message.media, offset=offset):
                        offset += chunk.nbytes
                        out.write(chunk)
                        self.progress(offset, message.media.document.size)
                    self.download_finished(message)
