import os

import aiohttp

from routers.base_message_router import BaseMessageRouter


class StartRouter(BaseMessageRouter):
    """
    Роутер для команды /start
    """

    HOST = os.getenv("HOST")
    USERS_PATH = "api/v1/users/"

    def __init__(self, message):
        super().__init__(message)

    async def route(self) -> None:
        """
        См. Документацию в абстрактном классе BaseMessageRouter

        :return: None
        """

        if await self.__user_exists(self.__message.get_from_user().get_id()):
            await self.__send_hello_message()
            return

        if self.__message.get_args():
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

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{StartRouter.HOST}{StartRouter.USERS_PATH}{user_id}"
            ) as response:
                return True if response.status == 200 else False

    async def __send_hello_message(self) -> None:
        pass

    async def __create_user(self) -> None:
        """
        Создать нового пользователя на сервере

        :return: None
        """

        request_json = {
            "user_id": self.__message.get_from_user().get_id(),
            "username": self.__message.get_from_user().get_username(),
            "fullname": self.__message.get_from_user().get_full_name(),
            "language": self.__message.get_from_user().get_language_code()
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f"{StartRouter.HOST}{StartRouter.USERS_PATH}",
                    json=request_json
            ):
                pass

    async def create_user_with_ref_code(self) -> None:
        """
        Создать на сервере пользователя присоединившегося по реферальной ссылке

        :return: None
        """

        # Валидаця рефки
        ref_is_digit: bool = self.__message.get_args().isdigit()
        user_exists: bool = await self.__user_exists(int(self.__message.get_args()))

        # если рефка не валидна, создаем юзера без рефки
        if not ref_is_digit or not user_exists:
            await self.__create_user()
            return

        # формируем и отправляем запрос
        request_json = {
            "user_id": self.__message.get_from_user().get_id(),
            "username": self.__message.get_from_user().get_username(),
            "fullname": self.__message.get_from_user().get_full_name(),
            "language": self.__message.get_from_user().get_language_code(),
            "ref_user": int(self.__message.get_args())
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f"{StartRouter.HOST}{StartRouter.USERS_PATH}",
                    json=request_json
            ):
                pass

