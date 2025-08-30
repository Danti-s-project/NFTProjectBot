from abc import ABC

from aiogram.types import CallbackQuery

from routers.IRouter import IRouter
from abstraction.Aiogram3CallbackQuery import Aiogram3CallbackQuery


class BaseCallbackQueryRouter(IRouter, ABC):
    """
    Абстрактный класс для всех callback query роутеров
    """
    def __init__(self, callback_query: CallbackQuery):
        self._callback_query: Aiogram3CallbackQuery = Aiogram3CallbackQuery(callback_query)
