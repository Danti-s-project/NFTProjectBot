from aiogram.filters.callback_data import CallbackData as AiogramCallbackData

from abstraction.callbacks.ICallbackData import ICallbackData


class CallbackData(AiogramCallbackData, ICallbackData):
    """
    Базовый класс для всех классов с припиской CallbackData
    """
    pass