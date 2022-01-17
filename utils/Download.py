from pathlib import Path
from utils import bytes_to
from utils import logger
from utils.MetadataDownload import MetadataDownload
from telethon import TelegramClient
from telethon.tl.custom.message import Message
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class Download(MetadataDownload):
    def __init__(self):
        self.file = ""

    def make_directory(self, abs_path: Path):
        abs_path.parent.mkdir(parents=True, exist_ok=True)

    def progress(self, current, total):
        current_m = bytes_to(current, "m")
        total_b = bytes_to(total, "m")
        path = "/".join(str(self.file).split("/")[-3:])
        logger.info("Download total: {}% {} mb/{} mb {}"
                    .format(int((current / total) * 100), current_m, total_b, path))

    async def download_file(self, client: TelegramClient, message: Message, abs_path=None):
        if not self.already_downloaded(message):
            path = abs_path
            if path:
                with open(path, "wb") as out:
                    if config["Telegram"]["APP_DEBUG"] != "true":
                        self.start_download(message)
                        self.file = path
                        logger.info("Inicio de descarga de archivo")
                        await client.download_media(message.media.document, out, progress_callback=self.progress)
                        logger.info("Finalización de descarga de archivo")
                    self.download_finished(message)
