from channels.ChannelFatory import ChannelFactory
from pathlib import Path, PurePath
from telethon.tl.custom.message import Message
from telethon import TelegramClient
from utils.FileMimeType import FileMimeType
from utils.FastTelethon import download_file
from utils import bytes_to
from utils import logger
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class OnePiece(ChannelFactory):
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.show = "One Piece"
        self.parent = "Anime"
        self.file = ""

    def make_directory(self, abs_path: Path):
        abs_path.parent.mkdir(parents=True, exist_ok=True)

    def progress(self, current, total):
        current_m = bytes_to(current, "m")
        total_b = bytes_to(total, "m")
        path = "/".join(str(self.file).split("/")[-3:])
        logger.info("Download total: {}% {} mb/{} mb {}"
                    .format(int((current / total) * 100), current_m, total_b, path))

    async def download_file(self, client: TelegramClient, message: Message, abs_path):
        if not self.already_downloaded(message) and not self.must_ignore(message):
            path = self.get_path(message)
            # if path:
            #     with open(path, "wb") as out:
            #         if config["Telegram"]["APP_DEBUG"] != "true":
            #             self.start_download(message)
            #             self.file = path
            #             logger.info("Inicio de descarga de archivo")
            #             await download_file(client, message.media.document, out, progress_callback=self.progress)
            #             logger.info("Finalización de descarga de archivo")
            #         self.download_finished(message)

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
            self.make_directory(abs_path)
            return Path(abs_path)
