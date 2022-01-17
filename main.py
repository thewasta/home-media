#!/usr/bin/env python3.8
import asyncio
import configparser
from pathlib import Path

import psutil
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel

from channels.ChannelFatory import ChannelFactory
from channels.DisneyPalomitas import DisneyPalomitas
from channels.OnePiece import OnePiece
from channels.YoungSheldon import YoungSheldon
from utils import bytes_to
from utils.Download import Download
from utils.Logger import setup_logger

config = configparser.ConfigParser()
config.read("config.ini")
loop = asyncio.get_event_loop()
api_id = int(config['Telegram']['API_TOKEN'])
api_hash = str(config['Telegram']['API_HASH'])
channels_videos = config["Channels"]
disk_usage = int(config['Telegram']['DISK_USAGE'])

client = TelegramClient("session", api_id, api_hash)
logger = setup_logger("main")

channels_factories = {
    config["Channels"]["one_piece"]: OnePiece(config["Channels"]["one_piece"]),
    config["Channels"]["young_sheldon"]: YoungSheldon(config["Channels"]["young_sheldon"]),
    config["Channels"]["disney_palomitas"]: DisneyPalomitas(config["Channels"]["disney_palomitas"]),
    config["Channels"]["zuby_palomitas"]: DisneyPalomitas(config["Channels"]["zuby_palomitas"]),
}


def check_file_exist(abs_path):
    return Path(abs_path).exists()


async def get_dialogs():
    async for chat in client.iter_dialogs():
        with open("storage/data.txt", "a") as file:
            file.write(f'{chat.name} has ID {chat.id}')
            file.close()


def disk_full():
    hdd = psutil.disk_usage(config['Telegram']['DISK'])
    if hdd.percent >= disk_usage:
        raise f"Disk usage is over {disk_usage}%"


async def file_system_notification() -> bool:
    hdd = psutil.disk_usage(config['Telegram']['DISK'])
    result = False
    if hdd.percent >= disk_usage:
        result = True
        message = f"""
        ```
        Espacio en disco ya está al {hdd.percent}% 
        Total (GB) {bytes_to(hdd.total, "g")}
        Disponible (GB) {bytes_to(hdd.free, "g")}
        ```
        """
        await client.send_message("me", message)
    return result


async def main():
    download = Download()
    for channel, channel_id in channels_videos.items():
        peer_channel = PeerChannel(channel_id=int(channel_id))
        # todo REMOVE LIMIT WHEN READY TO PRODUCTION
        """
        :param message Message
        """
        async for message in client.iter_messages(entity=peer_channel):
            disk_full()
            await file_system_notification()
            if is_media_message(message):
                factory: ChannelFactory = channels_factories[channel_id]
                path = factory.get_path(message)
                if path and not factory.must_ignore(message):
                    if config["Telegram"]["APP_DEBUG"] != "true":
                        logger.info(f"Canal: {peer_channel.channel_id} Mensaje: {message.media.document.id}")
                        await download.download_file(client, message, path)


def is_media_message(message):
    media = message.media
    return media and not hasattr(media, 'photo') and not hasattr(media, "webpage")


if __name__ == "__main__":
    client.start()
    loop.run_until_complete(main())
