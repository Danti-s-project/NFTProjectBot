from abc import ABC, abstractmethod
from typing import Any, Optional

from abstraction.IUser import IUser


class IMessageAdapter(ABC):
    """
    Интерфейс-адаптер для объектов Message телеграмм-мессенджера
    """

    @abstractmethod
    def get_text(self) -> Optional[str]:
        """
        Получить текст сообщения

        Returns:
            Optional[str]: Текст сообщения или None, если сообщение не содержит текста
        """
        pass

    @abstractmethod
    def get_chat_id(self) -> int:
        """
        Получить идентификатор чата, в котором отправлено сообщение

        Returns:
            int: Идентификатор чата
        """
        pass

    @abstractmethod
    def get_from_user(self) -> IUser:
        """
        Получить объект пользователя, отправившего сообщение

        Returns:
            IUser: Объект, реализующий интерфейс IUser
        """
        pass

    @abstractmethod
    async def answer(self, text: str, reply_markup=None) -> None:
        """
        Отправить ответ на сообщение пользователя
        :param text: текст сообщения для ответа
        :param reply_markup: клавиатура для ответа
        :return: None
        """
        pass

    @abstractmethod
    async def edit_reply_markup(self, reply_markup) -> None:
        """
        Редактировать inline кнопки под сообщением

        :param reply_markup: новая inline клавиатура под сообщением
        :return: None
        """
        pass

    @abstractmethod
    async def edit_message(self, text: str = None, reply_markup = None) -> None:
        """
        Редактировать текст сообщения

        :param reply_markup: объект клавиатуры
        :param text: новый текст сообщения
        :return: None
        """
        pass
