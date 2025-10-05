from typing import List, Any

from aiogram.types import ReplyKeyboardRemove as AiogramReplyKeyboardRemove

from abstraction.reply_keyboard.IReplyButton import IReplyButton
from abstraction.reply_keyboard.IReplyKeyboard import IReplyKeyboard


class ReplyKeyboardRemove(IReplyKeyboard):
    def get_keyboard_object(self) -> Any:
        return AiogramReplyKeyboardRemove()

    def add_buttons_row(self, buttons: List[IReplyButton]) -> 'IReplyKeyboard':
        raise NotImplementedError("Эту клавиатуру нельзя изменять!")

    def add_row(self) -> 'IReplyKeyboard':
        raise NotImplementedError("Эту клавиатуру нельзя изменять!")

    def add_button(self, button: IReplyButton) -> 'IReplyKeyboard':
        raise NotImplementedError("Эту клавиатуру нельзя изменять!")
