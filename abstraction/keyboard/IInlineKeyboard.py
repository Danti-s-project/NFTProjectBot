from abc import ABC, abstractmethod
from typing import Any, List

from abstraction.keyboard.IInlineButton import IInlineButton


class IInlineKeyboard(ABC):
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

    @abstractmethod
    def get_keyboard_object(self) -> Any:
        """
        Получить объект клавиатуры в формате, необходимом для конкретной реализации

        Returns:
            Any: Объект клавиатуры, готовый для использования в библиотеке
        """
        pass
