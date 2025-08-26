from abc import ABC, abstractmethod

from aiogram.types import Message

from abstraction.IMessage import IMessageAdapter
from abstraction.Aiogram3Message import Aiogram3MessageAdapter


class BaseMessageRouter(ABC):
    """
    Абстрактный.
    Все роутеры с припиской Message должны наследовать этот класс
    Для правильной работы
    """
    def __init__(self, message: Message):
        self.__message: IMessageAdapter = Aiogram3MessageAdapter(message) # Объявим тип

    @abstractmethod
    async def route(self) -> None:
        """
        Каждый роутер должен реализовывать этот метод
        Он должен вызываться сразу после создания экземпляра роутера

        Невозможность вызова этого метода в конструкторе обуславливается тем,
        что в конструкторе нельзя вызывать асинхронные методы
        Поэтому делаем фанкол
        :return: None
        """
        pass
