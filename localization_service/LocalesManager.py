from typing import Dict

from api.APIService import APIService
from localization_service.types import Locale

class LanguageManager:
    """
    Менеджер, кеширующий язык интерфейса пользователя в оперативной памяти,
    А также, предоставляющий интерфейс для работы с локалями
    Singleton
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(LanguageManager, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True
            self.__init(*args, **kwargs)

    def __init(self, *args, **kwargs):
        self.__locales: Dict[int, Locale] = {}  # TODO: Замени на hashmap с заданным размером

    async def get_locale(self, user_id: int) -> Locale:
        """
        Получить язык интерфейса пользователя из кеша, или если нет в кеше, из базы данных

        :param user_id: айди пользователя, чью локаль нужно получить
        :return: Locale
        """
        locale = self.__locales.get(user_id)

        if locale is None:
            user = await APIService().get_user(user_id)
            language = user.language
            match language:
                case "ru":
                    locale = Locale.RU
                case "en":
                    locale = Locale.EN
                case "zh":
                    locale = Locale.ZH
                case _:
                    locale = Locale.EN

            self.__locales[user_id] = locale

        return locale
