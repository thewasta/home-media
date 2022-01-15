from channels.ChannelFatory import ChannelFactory
from pathlib import Path
from utils.FastTelethon import download_file


class AnimeZuby(ChannelFactory):
    def __init__(self):
        self.show = "One Piece"

    def make_directory(self, abs_path: Path):
        ""

    async def download_file(self, client, message, abs_path):
        with open("file222.mp4", "wb") as out:
            await download_file(client, document, out)

    def get_path(self, abs_path) -> str:
        return self.show
