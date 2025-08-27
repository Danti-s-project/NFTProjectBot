from abc import ABC

from aiogram.types import Message

from abstraction.IMessage import IMessageAdapter
from abstraction.Aiogram3Message import Aiogram3MessageAdapter
from routers.IRouter import IRouter


class BaseMessageRouter(IRouter, ABC):
    """
    Абстрактный.
    Все роутеры с припиской Message должны наследовать этот класс
    Для правильной работы
    """
    def __init__(self, message: Message):
        self.__message: IMessageAdapter = Aiogram3MessageAdapter(message) # Объявим тип
