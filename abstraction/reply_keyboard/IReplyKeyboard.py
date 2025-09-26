from abc import ABC, abstractmethod
from typing import List
from aiogram.types import ReplyKeyboardMarkup

from abstraction.reply_keyboard.IReplyButton import IReplyButton


class IReplyKeyboard(ABC):
    """
    Интерфейс для обычной клавиатуры (ReplyKeyboardMarkup)
    """

    @abstractmethod
    def add_button(self, button: IReplyButton) -> 'IReplyKeyboard':
        """
        Добавить кнопку в текущий ряд клавиатуры
        """
        pass

    @abstractmethod
    def add_row(self) -> 'IReplyKeyboard':
        """
        Завершить текущий ряд и начать новый
        """
        pass

    @abstractmethod
    def add_buttons_row(self, buttons: List[IReplyButton]) -> 'IReplyKeyboard':
        """
        Добавить сразу ряд кнопок
        """
        pass

    @abstractmethod
    def get_keyboard_object(self) -> ReplyKeyboardMarkup:
        """
        Получить объект клавиатуры aiogram
        """
        pass
