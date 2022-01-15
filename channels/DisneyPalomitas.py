import re
from pathlib import Path, PurePath
from utils.FileMimeType import FileMimeType
from utils.FastTelethon import download_file
from telethon.tl.custom import Message

from channels.ChannelFatory import ChannelFactory
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class DisneyPalomitas(ChannelFactory):
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.show = ""
        self.parent = "TV Shows"

    async def download_file(self, client, message, abs_path: str):
        if not self.already_downloaded(message) and not self.must_ignore(message):
            path = self.get_path(message)
            # if path:
            #     with open(path, "wb") as out:
            #         self.start_download(message)
            #         if config["Telegram"]["APP_DEBUG"] != "true":
            #             print("DOWNLOAD", "DISNEY")
            #             exit()
            #             await download_file(client, message.media.document, out)
            #         self.download_finished(message)

    def make_directory(self, abs_path: Path):
        abs_path.parent.mkdir(parents=True, exist_ok=True)

    def must_ignore(self, message: Message) -> bool:
        if not hasattr(message.media.document.attributes[0], "file_name"):
            return True
        if "rar" in message.media.document.mime_type:
            return True
        message_file_name = message.media.document.attributes[0].file_name
        if "prano" in message_file_name or \
                "gitivo" in message_file_name or \
                "Hija" in message_file_name or \
                "7x22-Stargate" in message_file_name:
            return True
        if not re.search("(\d{1,2}x\d{1,2})", message_file_name):
            return True

    def get_path(self, message: Message):
        message_file_name = message.media.document.attributes[0].file_name
        file_type = FileMimeType.get_mime(message.media.document.mime_type)
        show_name_search = re.search("(\d{1,2}x\d{1,2})", message_file_name)
        if show_name_search:
            show_name_search = show_name_search.group()
            show_name_remove_chapter = message_file_name.replace(show_name_search, "")
            self.show = re.sub("\@.*", "", show_name_remove_chapter).strip()
            self.show = re.sub("[^a-zA-Z0-9,\s]", "", self.show)
            self.__rename_show()
            main_folder_path = PurePath(str(config['Telegram']['PATH']), self.parent, self.show)
            season = re.findall("\d{1,2}", message_file_name)[0]
            chapter = re.findall("\d{1,2}", message_file_name)[1]
            file_name = f"{self.show} S{season}E{chapter}.{file_type}"
            abs_path = Path(PurePath(main_folder_path, file_name))
            self.make_directory(abs_path)
            return Path(abs_path)

    def __rename_show(self):
        if "Hawaii" in self.show:
            self.show = "Hawaii Five Zero"
        if "Star Trek" in self.show:
            self.show = "Stark Trek"
        if "stacion" in self.show:
            self.show = "Estacion 19"
        if "Dark" in self.show and "Angel" in self.show:
            self.show = "Dark Angel"
        if "Hombres" in self.show and "Paco" in self.show:
            self.show = "Los Hombres de Paco"
        if "Madagascar" in self.show and "Salvajes" in self.show:
            self.show = "Madagascar pequeños salvajes"
        if "Manhunt" in self.show and "Unabomber" in self.show:
            self.show = "Manhunt Unabomber"
        if "Operac" in self.show and "xtasis" in self.show:
            self.show = "Operacion extasis"
        if "TGDoctor" in self.show:
            self.show = "The Good Doctor"
