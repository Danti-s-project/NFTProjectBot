from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from abc import ABC
from routers.IRouter import IRouter
from abstraction.Aiogram3Message import IMessageAdapter, Aiogram3MessageAdapter
from abstraction.fsm.FSMFactory import FSMFactory

# TODO: заменить конкретное упоминание Aiogram3MessageAdapter и подобных на фабрики во избежание конкретики

class BaseFSMRouter(IRouter, ABC):
    """
    Базовый роутер для fsm

    """

    def __init__(self, message: Message, fsm: FSMContext):
        self._message: IMessageAdapter = Aiogram3MessageAdapter(message)
        self._fsm = FSMFactory.create_fsm(fsm)
