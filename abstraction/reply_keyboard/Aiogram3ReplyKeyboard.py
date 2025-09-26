from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from abstraction.reply_keyboard.IReplyButton import IReplyButton
from abstraction.reply_keyboard.IReplyKeyboard import IReplyKeyboard


class Aiogram3ReplyKeyboard(IReplyKeyboard):
    """
    Адаптер для обычной клавиатуры (ReplyKeyboardMarkup) aiogram 3.x
    """

    def __init__(self, resize_keyboard: bool = True, one_time_keyboard: bool = False):
        self._keyboard: List[List[KeyboardButton]] = []
        self._current_row: List[KeyboardButton] = []
        self._resize_keyboard = resize_keyboard
        self._one_time_keyboard = one_time_keyboard

    def add_button(self, button: IReplyButton) -> 'Aiogram3ReplyKeyboard':
        self._current_row.append(button.get_button_object())
        return self

    def add_row(self) -> 'Aiogram3ReplyKeyboard':
        if self._current_row:
            self._keyboard.append(self._current_row)
            self._current_row = []
        return self

    def add_buttons_row(self, buttons: List[IReplyButton]) -> 'Aiogram3ReplyKeyboard':
        if self._current_row:
            self._keyboard.append(self._current_row)
            self._current_row = []

        row = [button.get_button_object() for button in buttons]
        self._keyboard.append(row)
        return self

    def get_keyboard_object(self) -> ReplyKeyboardMarkup:
        keyboard = self._keyboard.copy()
        if self._current_row:
            keyboard.append(self._current_row)

        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=self._resize_keyboard,
            one_time_keyboard=self._one_time_keyboard
        )
    