from aiogram.types import KeyboardButton

from abstraction.reply_keyboard.IReplyButton import IReplyButton


class Aiogram3ReplyButton(IReplyButton):
    """
    Адаптер для кнопки обычной клавиатуры aiogram 3.x
    """

    def __init__(self):
        self._text: str = ""
        self._request_contact: bool = False
        self._request_location: bool = False

    def set_text(self, text: str) -> 'Aiogram3ReplyButton':
        self._text = text
        return self

    def request_contact(self, value: bool = True) -> 'Aiogram3ReplyButton':
        self._request_contact = value
        return self

    def request_location(self, value: bool = True) -> 'Aiogram3ReplyButton':
        self._request_location = value
        return self

    def get_button_object(self) -> KeyboardButton:
        return KeyboardButton(
            text=self._text,
            request_contact=self._request_contact,
            request_location=self._request_location
        )
