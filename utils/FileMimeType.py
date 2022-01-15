class FileMimeType:
    @staticmethod
    def get_mime(mime: str):
        formats = {
            "x-matroska": "mkv",
            "x-msvideo": "avi"
        }
        split_mime = mime.split("/")
        if split_mime[1] in formats:
            return formats[split_mime[1]]
        return split_mime[1]
