from abc import ABC

from aiogram.types import Message

from abstraction.message.IMessage import IMessageAdapter
from abstraction.message.MessageFactory import MessageFactory
from routers.IRouter import IRouter


class BaseMessageRouter(IRouter, ABC):
    """
    Абстрактный.
    Все роутеры с припиской Message должны наследовать этот класс
    Для правильной работы
    """
    def __init__(self, message: Message):
        self._message: IMessageAdapter = MessageFactory().get(message) # Объявим тип
