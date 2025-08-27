from abc import ABC, abstractmethod

from aiogram.filters.callback_data import CallbackData


class ICallbackData(ABC):
    """
    Интерфейс для классов с припиской CallbackData
    Он взят из aiogram 3.x
    """

    @abstractmethod
    def pack(self):
        """
        Generate callback data string

        :return: valid callback data for Telegram Bot API
        """
        pass

    @abstractmethod
    def unpack(self, value: str):
        """
        Parse callback data string

        :param value: value from Telegram
        :return: instance of CallbackData
        """
        pass
