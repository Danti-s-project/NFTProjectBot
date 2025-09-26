from aiogram.types import InlineKeyboardButton

from abstraction.inline_keyboard.IInlineButton import IInlineButton


class Aiogram3InlineButton(IInlineButton):
    """
    Адаптер для инлайн-кнопок библиотеки aiogram 3.x
    """

    def __init__(self):
        """
        Инициализация адаптера для инлайн-кнопки
        """
        self._text = ""
        self._callback_data = None
        self._url = None

    def set_text(self, text: str) -> 'Aiogram3InlineButton':
        """
        Установить текст кнопки

        Args:
            text: Текст, отображаемый на кнопке

        Returns:
            Aiogram3InlineButton: Текущий объект кнопки для цепочки вызовов
        """
        self._text = text
        return self

    def set_callback_data(self, callback_data: str) -> 'Aiogram3InlineButton':
        """
        Установить данные обратного вызова для кнопки

        Args:
            callback_data: Строка с данными, которые будут отправлены при нажатии на кнопку

        Returns:
            Aiogram3InlineButton: Текущий объект кнопки для цепочки вызовов
        """
        self._callback_data = callback_data
        self._url = None  # URL и callback_data взаимоисключающие
        return self

    def set_url(self, url: str) -> 'Aiogram3InlineButton':
        """
        Установить URL для кнопки

        Args:
            url: Ссылка, на которую будет перенаправлен пользователь при нажатии

        Returns:
            Aiogram3InlineButton: Текущий объект кнопки для цепочки вызовов
        """
        self._url = url
        self._callback_data = None  # URL и callback_data взаимоисключающие
        return self

    def get_button_object(self) -> InlineKeyboardButton:
        """
        Получить объект кнопки aiogram

        Returns:
            InlineKeyboardButton: Объект инлайн-кнопки aiogram

        Raises:
            ValueError: Если текст кнопки не задан или не заданы ни callback_data, ни url
        """
        if not self._text:
            raise ValueError("Текст кнопки должен быть задан")

        kwargs = {}

        if self._callback_data is not None:
            kwargs['callback_data'] = self._callback_data
        elif self._url is not None:
            kwargs['url'] = self._url

        return InlineKeyboardButton(text=self._text, **kwargs)
