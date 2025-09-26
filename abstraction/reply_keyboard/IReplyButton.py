from abc import ABC, abstractmethod
from aiogram.types import KeyboardButton


class IReplyButton(ABC):
    """
    Интерфейс для кнопки обычной клавиатуры (ReplyKeyboard)
    """

    @abstractmethod
    def set_text(self, text: str) -> 'IReplyButton':
        """
        Установить текст кнопки
        """
        pass

    @abstractmethod
    def request_contact(self, value: bool = True) -> 'IReplyButton':
        """
        Сделать кнопку запрашивающей контакт
        """
        pass

    @abstractmethod
    def request_location(self, value: bool = True) -> 'IReplyButton':
        """
        Сделать кнопку запрашивающей геолокацию
        """
        pass

    @abstractmethod
    def get_button_object(self) -> KeyboardButton:
        """
        Получить объект кнопки aiogram
        """
        pass
