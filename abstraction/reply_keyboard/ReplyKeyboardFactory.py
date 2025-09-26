from typing import List

from abstraction.reply_keyboard.Aiogram3ReplyKeyboard import Aiogram3ReplyKeyboard
from abstraction.reply_keyboard.Aiogram3ReplyButton import Aiogram3ReplyButton
from abstraction.reply_keyboard.IReplyKeyboard import IReplyKeyboard
from abstraction.reply_keyboard.IReplyButton import IReplyButton


class ReplyKeyboardFactory:
    """
    Фабрика для создания обычной клавиатуры и кнопок
    """

    @staticmethod
    def create_keyboard(resize_keyboard: bool = True, one_time_keyboard: bool = False) -> IReplyKeyboard:
        return Aiogram3ReplyKeyboard(resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard)

    @staticmethod
    def create_button(text: str = "", request_contact: bool = False, request_location: bool = False) -> IReplyButton:
        button = Aiogram3ReplyButton().set_text(text)

        if request_contact:
            button.request_contact(True)
        if request_location:
            button.request_location(True)

        return button

    @staticmethod
    def create_buttons_row(buttons_data: List[dict]) -> List[IReplyButton]:
        """
        Создать ряд кнопок из словарей с данными

        Args:
            buttons_data: Список словарей с данными для кнопок
                Каждый словарь должен содержать 'text' и опционально 'request_contact'/'request_location'
        """
        buttons = []
        for data in buttons_data:
            text = data.get('text', '')
            request_contact = data.get('request_contact', False)
            request_location = data.get('request_location', False)

            button = ReplyKeyboardFactory.create_button(text, request_contact, request_location)
            buttons.append(button)

        return buttons
