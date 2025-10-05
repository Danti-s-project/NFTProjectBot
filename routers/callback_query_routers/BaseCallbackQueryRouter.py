from abc import ABC
from typing import Optional

from aiogram.types import CallbackQuery

from routers.IRouter import IRouter
from aiogram.fsm.context import FSMContext
from abstraction.callback_query.ICallbackQuery import ICallbackQuery
from abstraction.callback_query.CallbackQueryFactory import CallbackQueryFactory


class BaseCallbackQueryRouter(IRouter, ABC):
    """
    Абстрактный класс для всех callback query роутеров
    """
    def __init__(self, callback_query: CallbackQuery, fsm_state: Optional[FSMContext] = None):
        self._callback_query: ICallbackQuery = CallbackQueryFactory().get(callback_query)
        self._fsm_state = fsm_state
