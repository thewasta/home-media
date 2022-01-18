from abc import ABC, abstractmethod

from telethon.tl.custom.message import Message


class ChannelFactory(ABC):
    @abstractmethod
    def must_ignore(self, message: Message) -> bool:
        """
        :param message:
        :return:
        """

    @abstractmethod
    def get_path(self, message: Message):
        """"""
