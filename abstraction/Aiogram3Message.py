from typing import Optional

from aiogram.types import Message

from abstraction.Aiogram3User import Aiogram3User
from abstraction.IMessage import IMessageAdapter
from abstraction.keyboard.IInlineKeyboard import IInlineKeyboard
from abstraction.IUser import IUser


class Aiogram3MessageAdapter(IMessageAdapter):
    """
    Адаптер для объекта Message из библиотеки aiogram версии 3.x
    """

    def __init__(self, message: Message):
        """
        Инициализация адаптера для сообщения

        Args:
            message (Message): Объект сообщения aiogram
        """
        self._message = message

    def get_text(self) -> Optional[str]:
        """
        Получить текст сообщения

        Returns:
            Optional[str]: Текст сообщения или None, если сообщение не содержит текста
        """
        return self._message.text

    def get_chat_id(self) -> int:
        """
        Получить идентификатор чата, в котором отправлено сообщение

        Returns:
            int: Идентификатор чата
        """
        return self._message.chat.id

    def get_from_user(self) -> IUser:
        """
        Получить объект пользователя, отправившего сообщение

        Returns:
            IUser: Объект пользователя в виде адаптера
        """
        return Aiogram3User(self._message.from_user)

    async def answer(self, text: str, reply_markup: IInlineKeyboard = None) -> None:
        """
        Отправить ответ на сообщение пользователя

        :param text: текст сообщения для ответа
        :param reply_markup: клавиатура для ответа
        :return: None
        """

        # Получаем aiogram клавиатуру
        if reply_markup:
            reply_markup = reply_markup.get_keyboard_object()

        await self._message.answer(text, reply_markup=reply_markup)

    async def edit_reply_markup(self, reply_markup: IInlineKeyboard) -> None:
        """
        Редактировать inline кнопки под сообщением

        :param reply_markup: новая inline клавиатура под сообщением
        :return: None
        """
        await self._message.edit_reply_markup(reply_markup=reply_markup.get_keyboard_object())

    async def edit_message_text(self, text: str) -> None:
        """
        Редактировать текст сообщения

        :param text: новый текст сообщения
        :return: None
        """
        await self._message.edit_text(text)

