import json

from localization_service.types import Locale, SystemMessages


class i18n:
    """
    Обратитесь к инстансу этого класса, чтобы получить нужное сообщение с локализацией
    Singleton, инициализируйте инстанс этого класса перед запуском бота
    """

    LOCALES_FILE_PATH = "i18n.json"

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(i18n, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance


    def __init__(self, *args, **kwargs):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True
            self.__init(*args, **kwargs)


    def __init(self, *args, **kwargs):
        # Загрузка локалей в оперативку

        with open(self.LOCALES_FILE_PATH, encoding="utf-8") as f:
            self.__locales = json.load(f)

    def get_text(self, message: SystemMessages, locale: Locale, *args) -> str:
        """
        Получите сообщение на указанном языке

        :param message: Конкретное сообщение, которое нам нужно.
        :param locale: Язык, на котором нужно получить сообщение.
        :param args: Значения, которые нужно подставить в сообщение на нужные места.
        :return: Текст сообщения на нужном языке
        """

        message_localizations = self.__locales[message.value][locale.value]
        return message_localizations.format(*args)
