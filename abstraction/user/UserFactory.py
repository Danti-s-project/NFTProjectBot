from abstraction.user.Aiogram3User import Aiogram3User
from abstraction.user.IUser import IUser

class UserFactory:
    """
    Фабрика скрывает реализацию, и отдает объект реализующий нужный интерфейс
    Singleton
    """

    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super(UserFactory, cls).__new__(cls)
            cls._initialized = False
        return cls._instance

    def __init__(self):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True

    def get(self, *args, **kwargs) -> IUser:
        """
        Метод получения нужного объекта

        :return: ICallbackQuery
        """
        return Aiogram3User(*args, **kwargs)