import os
import typing

from aiogram.filters import CommandObject

from api.APIService import APIService
from localization_service import i18n, SystemMessages, LocalesManager
from routers.message_routers.BaseMessageRouter import BaseMessageRouter


class StartRouterWithDeepLink(BaseMessageRouter):
    """
    Роутер для команды /start
    """

    HOST = os.getenv("HOST")
    USERS_PATH = "api/v1/users/"

    def __init__(self, message, command: typing.Optional[CommandObject] = None):
        """
        Конструктор роутера для команды /start с deep_link
        Используется дополнительный параметр command для создания реферальных ссылок.
        По возможности исключите прямое взаимодействие с API

        :param message: aiogram.types.Message
        :param command: aiogram.filter.CommandStart
        """
        super().__init__(message)

        self.__command: CommandObject = command

    async def route(self) -> None:
        """
        См. Документацию в абстрактном классе BaseMessageRouter

        :return: None
        """

        # Если пользователь уже регистрировался
        if await self.__user_exists(self._message.get_from_user().get_id()):
            await self.__send_hello_message()
            return

        if self.__command:
            await self.create_user_with_ref_code()
        else:
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
        locale = await LocalesManager().get_locale(self._message.get_from_user().get_id())
        message = i18n().get_text(SystemMessages.START_MESSAGE, locale)

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

    async def create_user_with_ref_code(self) -> None:
        """
        Создать на сервере пользователя присоединившегося по реферальной ссылке

        :return: None
        """

        # Валидаця рефки
        ref_is_digit: bool = self.__command.args.isdigit()
        user_exists: bool = await self.__user_exists(int(self.__command.args))

        # если рефка не валидна, создаем юзера без рефки
        if not ref_is_digit or not user_exists:
            await self.__create_user()
            return

        # формируем и отправляем запрос
        request_json = {
            "user_id": self._message.get_from_user().get_id(),
            "username": self._message.get_from_user().get_username(),
            "fullname": self._message.get_from_user().get_full_name(),
            "language": self._message.get_from_user().get_language_code(),
            "ref_user": int(self.__command.args)
        }

        await APIService().create_user(request_json)

