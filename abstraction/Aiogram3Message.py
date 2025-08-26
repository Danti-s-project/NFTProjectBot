from typing import Optional

from aiogram.types import Message

from abstraction.Aiogram3User import Aiogram3User
from abstraction.IMessage import IMessageAdapter
from abstraction.IUser import IUser


class Aiogram3MessageAdapter(IMessageAdapter):
    """
    Адаптер для объекта Message из библиотеки aiogram версии 3.x
    """

    def __init__(self, message: Message, command_args: Optional[str] = None):
        """
        Инициализация адаптера для сообщения

        Args:
            message (Message): Объект сообщения aiogram
            command_args (Optional[str]) именнованный аргумент
        """
        self._message = message
        self.__command_args = command_args

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

    def get_args(self) -> Optional[str]:
        """
        Получить аргументы отправленные с командой
        Например реферальная ссылка t.me/<bot_username>?start=<ref_code>

        :return: вернет аргумент команды или ref_code
        """
        return self.__command_args

    async def answer(self, text) -> None:
        """
        Отправить ответ на сообщение пользователя

        :return:
            None
        """
        await self._message.answer(text)

