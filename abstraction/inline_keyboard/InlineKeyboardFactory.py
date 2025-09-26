from typing import List, Optional

from abstraction.inline_keyboard.Aiogram3InlineButton import Aiogram3InlineButton
from abstraction.inline_keyboard.Aiogram3InlineKeyboard import Aiogram3InlineKeyboard
from abstraction.inline_keyboard.IInlineButton import IInlineButton
from abstraction.inline_keyboard.IInlineKeyboard import IInlineKeyboard


class InlineKeyboardFactory:
    """
    Фабрика для создания инлайн-клавиатуры и кнопок
    """

    @staticmethod
    def create_keyboard() -> IInlineKeyboard:
        """
        Создать новую инлайн-клавиатуру

        Returns:
            IInlineKeyboard: Объект инлайн-клавиатуры
        """
        return Aiogram3InlineKeyboard()

    @staticmethod
    def create_button(text: str = "", callback_data: Optional[str] = None, url: Optional[str] = None) -> IInlineButton:
        """
        Создать новую инлайн-кнопку

        Args:
            text: Текст кнопки
            callback_data: Данные обратного вызова
            url: URL для кнопки

        Returns:
            IInlineButton: Объект инлайн-кнопки

        Note:
            callback_data и url являются взаимоисключающими
        """
        button = Aiogram3InlineButton()

        if text:
            button.set_text(text)

        if callback_data is not None:
            button.set_callback_data(callback_data)
        elif url is not None:
            button.set_url(url)

        return button

    @staticmethod
    def create_buttons_row(buttons_data: List[dict]) -> List[IInlineButton]:
        """
        Создать ряд кнопок из словарей с данными

        Args:
            buttons_data: Список словарей с данными для кнопок
                Каждый словарь должен содержать ключ 'text' и может содержать
                'callback_data' или 'url'

        Returns:
            List[IInlineButton]: Список объектов инлайн-кнопок
        """
        buttons = []

        for data in buttons_data:
            text = data.get('text', '')
            callback_data = data.get('callback_data')
            url = data.get('url')

            button = InlineKeyboardFactory.create_button(text, callback_data, url)
            buttons.append(button)

        return buttons
