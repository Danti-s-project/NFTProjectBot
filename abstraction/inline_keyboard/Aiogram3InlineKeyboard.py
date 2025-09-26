from typing import List

from aiogram.types import InlineKeyboardMarkup

from abstraction.inline_keyboard.IInlineButton import IInlineButton
from abstraction.inline_keyboard.IInlineKeyboard import IInlineKeyboard


class Aiogram3InlineKeyboard(IInlineKeyboard):
    """
    Адаптер для инлайн-клавиатуры библиотеки aiogram 3.x
    """

    def __init__(self):
        """
        Инициализация адаптера для инлайн-клавиатуры
        """
        self._keyboard = []
        self._current_row = []

    def add_button(self, button: IInlineButton) -> 'Aiogram3InlineKeyboard':
        """
        Добавить кнопку в текущий ряд клавиатуры

        Args:
            button: Кнопка для добавления

        Returns:
            Aiogram3InlineKeyboard: Текущий объект клавиатуры для цепочки вызовов
        """
        self._current_row.append(button.get_button_object())
        return self

    def add_row(self) -> 'Aiogram3InlineKeyboard':
        """
        Добавить новый ряд кнопок в клавиатуру

        Returns:
            Aiogram3InlineKeyboard: Текущий объект клавиатуры для цепочки вызовов
        """
        if self._current_row:
            self._keyboard.append(self._current_row)
            self._current_row = []
        return self

    def add_buttons_row(self, buttons: List[IInlineButton]) -> 'Aiogram3InlineKeyboard':
        """
        Добавить ряд кнопок в клавиатуру

        Args:
            buttons: Список кнопок для добавления в один ряд

        Returns:
            Aiogram3InlineKeyboard: Текущий объект клавиатуры для цепочки вызовов
        """
        # Сначала сохраняем текущий ряд, если он не пустой
        if self._current_row:
            self._keyboard.append(self._current_row)
            self._current_row = []

        # Добавляем новый ряд из переданных кнопок
        row = [button.get_button_object() for button in buttons]
        self._keyboard.append(row)

        return self

    def get_keyboard_object(self) -> InlineKeyboardMarkup:
        """
        Получить объект клавиатуры aiogram

        Returns:
            InlineKeyboardMarkup: Объект инлайн-клавиатуры aiogram
        """
        # Добавляем текущий ряд, если он не пустой
        keyboard = self._keyboard.copy()
        if self._current_row:
            keyboard.append(self._current_row)

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
