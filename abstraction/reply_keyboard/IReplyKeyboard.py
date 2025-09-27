from abc import ABC, abstractmethod
from typing import List
from aiogram.types import ReplyKeyboardMarkup

from abstraction.reply_keyboard.IReplyButton import IReplyButton
from abstraction.IKeyboard import IKeyboard


class IReplyKeyboard(IKeyboard, ABC):
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
