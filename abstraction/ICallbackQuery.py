from abc import ABC, abstractmethod
from typing import Optional

from abstraction.IMessage import IMessageAdapter
from abstraction.IUser import IUser


class ICallbackQuery(ABC):
    """
    Интерфейс-адаптер для объектов CallbackQuery телеграмм-мессенджера
    """

    @abstractmethod
    def get_id(self) -> str:
        """
        Получить идентификатор callback запроса

        Returns:
            str: Идентификатор callback запроса
        """
        pass

    @abstractmethod
    def get_from_user(self) -> IUser:
        """
        Получить объект пользователя, который отправил callback запрос

        Returns:
            IUser: Объект, реализующий интерфейс IUser
        """
        pass

    @abstractmethod
    def get_message(self) -> Optional[IMessageAdapter]:
        """
        Получить сообщение, к которому относится callback запрос

        Returns:
            Optional[IMessageAdapter]: Объект сообщения или None, если запрос не связан с сообщением
        """
        pass

    @abstractmethod
    def get_data(self) -> Optional[str]:
        """
        Получить callback_data из callback запроса

        Returns:
            Optional[str]: callback_data или None, если данные отсутствуют
        """
        pass

    @abstractmethod
    async def answer(self, text: Optional[str] = None, show_alert: bool = False) -> None:
        """
        Ответить на callback запрос

        Args:
            text: Текст уведомления, которое будет показано пользователю
            show_alert: Если True, то будет показано модальное окно с уведомлением

        Returns:
            None
        """
        pass
