from abc import ABC, abstractmethod
from pathlib import Path
from utils.DownloadFile import DownloadFile
from telethon.tl.custom.message import Message


class ChannelFactory(ABC, DownloadFile):
    @abstractmethod
    async def download_file(self, client, message, abs_path: str):
        """
        Giving a document media, download file
        :param abs_path:
        :param client:
        :param message:
        :return:
        """

    @abstractmethod
    def make_directory(self, abs_path: Path):
        """
        Check if parents from absolute path exist, otherwise
        create directory
        :param abs_path:
        """

    @abstractmethod
    def should_ignore(self, message: Message) -> bool:
        """
        :param message:
        :return:
        """
