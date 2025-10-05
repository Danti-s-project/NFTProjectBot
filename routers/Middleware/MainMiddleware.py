from typing import Callable, Awaitable, Dict, Any

from aiogram.types import Message, CallbackQuery
from aiogram import BaseMiddleware
from api.APIService import APIService

class MainMiddleware(BaseMiddleware):
    """
    middleware для обработки сообщений
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event,
        data: Dict[str, Any]
    ) -> Any:

        # Если это команда /start - пускаем
        if isinstance(event, Message):
            if event.text.startswith("/start"):
                return await handler(event, data)

        # Проверяем зарегистрирован ли пользователь
        if not await APIService().get_user(event.from_user.id):
            await event.answer("Please, send /start command first")
            return None

        # Иначе вызываем его
        return await handler(event, data)
