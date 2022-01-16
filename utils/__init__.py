from utils.Logger import setup_logger

logger = setup_logger("main")


def bytes_to(bytes, to, bsize=1024):
    a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
    return format(bytes / (bsize ** a[to]), ".2f")
