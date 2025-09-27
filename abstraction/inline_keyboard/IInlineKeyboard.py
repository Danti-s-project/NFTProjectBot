from abc import ABC, abstractmethod
from typing import List

from abstraction.inline_keyboard.IInlineButton import IInlineButton
from abstraction.IKeyboard import IKeyboard

class IInlineKeyboard(IKeyboard, ABC):
    """
    Интерфейс для инлайн-клавиатуры в мессенджере
    """

    @abstractmethod
    def add_button(self, button: IInlineButton) -> 'IInlineKeyboard':
        """
        Добавить кнопку в текущий ряд клавиатуры

        Args:
            button: Кнопка для добавления

        Returns:
            IInlineKeyboard: Текущий объект клавиатуры для цепочки вызовов
        """
        pass

    @abstractmethod
    def add_row(self) -> 'IInlineKeyboard':
        """
        Добавить новый ряд кнопок в клавиатуру

        Returns:
            IInlineKeyboard: Текущий объект клавиатуры для цепочки вызовов
        """
        pass

    @abstractmethod
    def add_buttons_row(self, buttons: List[IInlineButton]) -> 'IInlineKeyboard':
        """
        Добавить ряд кнопок в клавиатуру

        Args:
            buttons: Список кнопок для добавления в один ряд

        Returns:
            IInlineKeyboard: Текущий объект клавиатуры для цепочки вызовов
        """
        pass
