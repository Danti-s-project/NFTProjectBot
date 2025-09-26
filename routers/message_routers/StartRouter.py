import os

from api.APIService import APIService
from localization_service.LocalesManager import LocalesManager
from localization_service.i18n import i18n
from localization_service.types import SystemMessages, Locale
from routers.message_routers.BaseMessageRouter import BaseMessageRouter


class StartRouter(BaseMessageRouter):
    """
    Роутер для команды /start
    """

    HOST = os.getenv("HOST")
    USERS_PATH = "api/v1/users/"

    def __init__(self, message):
        """
        Конструктор роутера для команды /start
        По возможности исключите прямое взаимодействие с API

        :param message: aiogram.types.Message
        """
        super().__init__(message)

    async def route(self) -> None:
        """
        См. Документацию в абстрактном классе BaseMessageRouter

        :return: None
        """

        # Если пользователь уже регистрировался
        if await self.__user_exists(self._message.get_from_user().get_id()):
            await self.__send_hello_message()
            return

        await self.__create_user()
        await self.__send_hello_message()

    async def __user_exists(self, user_id: int) -> bool:
        """
        Проверка существования пользоавтеля в базе данных

        :param user_id: id пользователя, которого нужно найти в базе данных
        :return: True, если пользователь существует, иначе False
        """

        return bool(await APIService().get_user(user_id))

    async def __send_hello_message(self) -> None:
        # Пользователь может регистрироваться в боте первый раз. На сервере нет его locale. Если его нет, отправляем сообщение на англйиском

        if await self.__user_exists(self._message.get_from_user().get_id()):
            locale = await LocalesManager().get_locale(self._message.get_from_user().get_id())
            message = i18n().get_text(SystemMessages.START_MESSAGE, locale)
        else:
            message = i18n().get_text(SystemMessages.START_MESSAGE, Locale.EN)

        await self._message.answer(message)

    async def __create_user(self) -> None:
        """
        Создать нового пользователя на сервере

        :return: None
        """

        request_json = {
            "user_id": self._message.get_from_user().get_id(),
            "username": self._message.get_from_user().get_username(),
            "fullname": self._message.get_from_user().get_full_name(),
            "language": self._message.get_from_user().get_language_code()
        }

        await APIService().create_user(request_json)
