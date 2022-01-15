from telethon.tl.custom.message import Message
from pathlib import Path
import json


class DownloadFile:
    # noinspection PyMethodMayBeStatic
    def start_download(self, message: Message):
        peer_channel = message.peer_id.channel_id
        media_id = message.media.document.id
        json_data, file = self.__read_json_file(peer_channel)
        self.__save_starting(json_data, media_id, peer_channel)

    # noinspection PyMethodMayBeStatic
    def __save_finished(self, json_data, media_id, peer_channel):
        for i in json_data:
            if str(i["id"]) == str(media_id):
                i["status"] = "finished"
        self.__save_data_to_file(json_data, peer_channel)

    # noinspection PyMethodMayBeStatic
    def __save_starting(self, json_data, media_id, peer_channel):
        media_on_json_data = False
        if len(json_data) > 0:
            for i in json_data:
                if str(i["id"]) == str(media_id):
                    i["retry"] = int(i["retry"]) + 1
                    media_on_json_data = True
        else:
            media_on_json_data = True
            json_data.append({
                "id": media_id,
                "retry": 1,
                "status": "downloading"
            })
        if not media_on_json_data:
            json_data.append({
                "id": media_id,
                "retry": 1,
                "status": "downloading"
            })
        self.__save_data_to_file(json_data, peer_channel)

    # noinspection PyMethodMayBeStatic
    def __save_data_to_file(self, json_data, peer_channel):
        with open(f"storage/data/{peer_channel}.json", "w") as out:
            json.dump(json_data, out)

    # noinspection PyMethodMayBeStatic
    def download_finished(self, message: Message):
        peer_channel = message.peer_id.channel_id
        media_id = message.media.document.id
        json_data, file = self.__read_json_file(peer_channel)
        self.__save_finished(json_data, media_id, peer_channel)

    # noinspection PyMethodMayBeStatic
    def already_downloaded(self, message: Message) -> bool:
        media_id = message.media.document.id
        peer_channel = message.peer_id.channel_id
        json_data, file = self.__read_json_file(peer_channel)
        result = False
        if len(json_data) > 0:
            for i in json_data:
                if str(i["id"]) == str(media_id) and i["status"] == "finished":
                    result = True
        return result

    # noinspection PyMethodMayBeStatic
    def __read_json_file(self, peer_channel):
        file_path = f"storage/data/{peer_channel}.json"
        if not Path(file_path).exists():
            with open(file_path, "w+") as f:
                f.write("[]")
                f.close()
        file = open(file_path)
        data = json.load(file)
        return data, file
