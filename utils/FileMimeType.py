class FileMimeType:
    @staticmethod
    def get_mime(mime: str):
        formats = {
            "x-matroska": "mkv",
            "x-msvideo": "avi"
        }
        split_mime = mime.split("/")
        if hasattr(formats, split_mime[1]):
            return formats[split_mime[1]]
        return split_mime[1]
