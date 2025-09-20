import logging
from collections import OrderedDict

from api.APIService import APIService
from localization_service.types import Locale


logger = logging.getLogger('LocalesManager')


class LocalesManager:
    """
    Менеджер, кеширующий язык интерфейса пользователя в оперативной памяти,
    А также, предоставляющий интерфейс для работы с локалями
    Singleton
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(LocalesManager, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True
            self.__init(*args, **kwargs)

    def __init(self, *args, **kwargs):
        self.__capacity = 32676
        self.__locales: OrderedDict[int, Locale] = OrderedDict()
        logger.info("LocalesManager был инициализирован")

    async def get_locale(self, user_id: int) -> Locale:
        """
        Получить язык интерфейса пользователя из кеша, или если нет в кеше, из базы данных

        :param user_id: айди пользователя, чью локаль нужно получить
        :return: Locale
        """
        locale = self.__locales.get(user_id)
        
        if locale:
            self.__locales.move_to_end(user_id)

        else:
            user = await APIService().get_user(user_id)

            if not user:
                logger.critical("user object is None, exiting the program. Please check your API service!")
                raise Exception("User object is None, exiting the program. Please check your API service!")

            language = user.language
            match language:
                case "ru":
                    locale = Locale.RU
                case "en":
                    locale = Locale.EN
                case "zh":
                    locale = Locale.ZH
                case _:
                    logger.error(f"Запрошен неизвестный код языка - {language}")
                    locale = Locale.EN

            self.__locales[user_id] = locale

            if len(self.__locales) > self.__capacity:
                logger.debug("LRU cache overflow, cleaning up old entry")
                self.__locales.popitem(last=False)

        return locale
