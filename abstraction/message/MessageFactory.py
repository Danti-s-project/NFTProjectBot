from abstraction.message.IMessage import IMessageAdapter
from abstraction.message.Aiogram3Message import Aiogram3MessageAdapter


class MessageFactory:
    """
    Фабрика скрывает реализацию, и отдает объект реализующий нужный интерфейс
    Singleton
    """

    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super(MessageFactory, cls).__new__(cls)
            cls._initialized = False
        return cls._instance

    def __init__(self):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True

    def get(self, *args, **kwargs) -> IMessageAdapter:
        """
        Метод получения нужного объекта

        :return: IMessageAdapter
        """
        return Aiogram3MessageAdapter(*args, **kwargs)