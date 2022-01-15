from telethon.tl.custom.message import Message
from pathlib import Path
import json


class DownloadFile:
    # noinspection PyMethodMayBeStatic
    def start_download(self, message: Message):
        peer_channel = message.peer_id.channel_id
        media_id = message.media.document.id
        data, file = self.read_json_file(peer_channel)
        for i in data:
            if i["id"] == str(media_id):
                i["status"] = "downloading"
                i["retry"] = int(i["retry"]) + 1
            else:
                i["retry"] = 1
        file.close()
        with open(f"storage/data/{peer_channel}.json", "w") as out:
            json.dump(data, out)

    # noinspection PyMethodMayBeStatic
    def download_finished(self, message: Message):
        peer_channel = message.peer_id.channel_id
        media_id = message.media.document.id
        dump = {
            "id": media_id,
            "status": "done",
            "retry": 1
        }
        data, file = self.read_json_file(peer_channel)
        for i in data:
            if i["id"] == str(media_id):
                dump["retry"] += int(i["retry"])

    # noinspection PyMethodMayBeStatic
    def already_downloaded(self, message: Message, path: str) -> bool:
        media_id = message.media.document.id
        peer_channel = message.peer_id.channel_id
        result = False
        data, file = self.read_json_file(peer_channel)
        found_id = False
        for i in data:
            if i["id"] == str(media_id) and i["status"] == "done":
                found_id = True
                break
        if Path(path).exists() and found_id:
            result = True
        file.close()

        return result

    # noinspection PyMethodMayBeStatic
    def read_json_file(self, peer_channel):
        file = open(f"storage/data/{peer_channel}.json")
        data = json.load(file)
        return data, file
