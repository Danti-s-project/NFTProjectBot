from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from abc import ABC
from routers.IRouter import IRouter
from abstraction.message.Aiogram3Message import IMessageAdapter
from abstraction.message.MessageFactory import MessageFactory
from abstraction.fsm.FSMFactory import FSMFactory

# TODO: заменить конкретное упоминание Aiogram3MessageAdapter и подобных на фабрики во избежание конкретики

class BaseFSMRouter(IRouter, ABC):
    """
    Базовый роутер для fsm
    """

    def __init__(self, message: Message, fsm: FSMContext):
        self._message: IMessageAdapter = MessageFactory().get(message)
        self._fsm = FSMFactory.create_fsm(fsm)
