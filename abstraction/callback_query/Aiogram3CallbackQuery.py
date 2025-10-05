from typing import Optional

from aiogram.types import CallbackQuery

from abstraction.message.Aiogram3Message import Aiogram3MessageAdapter
from abstraction.user.Aiogram3User import Aiogram3User
from abstraction.callback_query.ICallbackQuery import ICallbackQuery
from abstraction.message.IMessage import IMessageAdapter
from abstraction.user.IUser import IUser


class Aiogram3CallbackQuery(ICallbackQuery):
    """
    Адаптер для объекта CallbackQuery из библиотеки aiogram версии 3.x
    """

    def __init__(self, callback_query: CallbackQuery):
        """
        Инициализация адаптера для объекта CallbackQuery

        Args:
            callback_query (CallbackQuery): Объект CallbackQuery aiogram
        """
        self._callback_query = callback_query

    def get_id(self) -> str:
        """
        Получить идентификатор callback запроса

        Returns:
            str: Идентификатор callback запроса
        """
        return self._callback_query.id

    def get_from_user(self) -> IUser:
        """
        Получить объект пользователя, который отправил callback запрос

        Returns:
            IUser: Объект, реализующий интерфейс IUser
        """
        return Aiogram3User(self._callback_query.from_user)

    def get_message(self) -> Optional[IMessageAdapter]:
        """
        Получить сообщение, к которому относится callback запрос

        Returns:
            Optional[IMessageAdapter]: Объект сообщения или None, если запрос не связан с сообщением
        """
        if self._callback_query.message:
            return Aiogram3MessageAdapter(self._callback_query.message)
        return None

    def get_data(self) -> Optional[str]:
        """
        Получить callback_data из callback запроса

        Returns:
            Optional[str]: callback_data или None, если данные отсутствуют
        """
        return self._callback_query.data

    async def answer(self, text: Optional[str] = None, show_alert: bool = False) -> None:
        """
        Ответить на callback запрос

        Args:
            text: Текст уведомления, которое будет показано пользователю
            show_alert: Если True, то будет показано модальное окно с уведомлением

        Returns:
            None
        """
        await self._callback_query.answer(text=text, show_alert=show_alert)
