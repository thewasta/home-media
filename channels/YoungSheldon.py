import re
from pathlib import Path, PurePath
from telethon.tl.custom import Message
from utils.FileMimeType import FileMimeType
from utils.FastTelethon import download_file
from utils import bytes_to
from utils import logger

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

    def progress(self, current, total):
        current_m = bytes_to(current, "m")
        total_b = bytes_to(total, "m")
        path = "/".join(str(self.file).split("/")[-3:])
        logger.info("Download total: {}% {} mb/{} mb {}"
                    .format(int((current / total) * 100), current_m, total_b, path))

    async def download_file(self, client, message, abs_path: str):
        if not self.already_downloaded(message) and not self.must_ignore(message):
            path = self.get_path(message)
            if path:
                with open(path, "wb") as out:
                    if config["Telegram"]["APP_DEBUG"] != "true":
                        self.start_download(message)
                        self.file = path
                        logger.info("Inicio de descarga de archivo")
                        await download_file(client, message.media.document, out, progress_callback=self.progress)
                        logger.info("Finalización de descarga de archivo")
                    self.download_finished(message)

    def make_directory(self, abs_path: Path):
        abs_path.parent.mkdir(parents=True, exist_ok=True)

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
            self.make_directory(abs_path)
            return Path(abs_path)
