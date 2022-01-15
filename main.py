import asyncio
import configparser
from pathlib import Path
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel
from utils.Logger import setup_logger
from channels.ChannelFatory import ChannelFactory
from channels.OnePiece import OnePiece
import psutil

config = configparser.ConfigParser()
config.read("config.ini")
loop = asyncio.get_event_loop()
api_id = int(config['Telegram']['API_TOKEN'])
api_hash = str(config['Telegram']['API_HASH'])
channels_videos = config["Channels"]
disk_usage = int(config['Telegram']['DISK_USAGE'])

client = TelegramClient("session", api_id, api_hash)
logger = setup_logger("telethon")

channels_factories = {
    config["Channels"]["one_piece"]: OnePiece(config["Channels"]["one_piece"]),
}


def bytes_to(bytes, to, bsize=1024):
    a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
    return format(bytes / (bsize ** a[to]), ".2f")


def check_file_exist(abs_path):
    return Path(abs_path).exists()


async def get_dialogs():
    async for chat in client.iter_dialogs():
        with open("storage/data.txt", "a") as file:
            file.write(f'{chat.name} has ID {chat.id}')
            file.close()


def disk_full():
    hdd = psutil.disk_usage(config['Telegram']['DISK'])
    if hdd.percent >= 95:
        raise "Disk usage is over 95%"


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
    for channel, channel_id in channels_videos.items():
        peer_channel = PeerChannel(channel_id=int(channel_id))
        # todo REMOVE LIMIT WHEN READY TO PRODUCTION
        async for message in client.iter_messages(entity=peer_channel, limit=4):
            disk_full()
            await file_system_notification()
            if is_media_message(message):
                factory: ChannelFactory = channels_factories[channel_id]
                await factory.download_file(client, message, config["Telegram"]["PATH"])


def is_media_message(message):
    media = message.media
    return media and not hasattr(media, 'photo') and not hasattr(media, "webpage")


if __name__ == "__main__":
    client.start()
    loop.run_until_complete(main())
