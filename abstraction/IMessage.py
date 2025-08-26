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
    def get_args(self) -> Optional[str]:
        """
        Получить аргументы отправленные с командой
        Например реферальная ссылка t.me/<bot_username>?start=<ref_code>

        :return: вернет аргумент команды или ref_code
        """
        pass

    @abstractmethod
    async def answer(self, text) -> None:
        """
        Отправить ответ на сообщение пользователя
        :return: None
        """
        pass
