"""
Здесь все хендлеры команд бота
"""

from aiogram.filters.command import CommandStart, CommandObject,  Command
from aiogram.types import Message, CallbackQuery

from routers.message_routers.StartRouter import StartRouter
from routers.message_routers.SearchRouter import SearchRouter
from callbacks.search_callbacks import ChoiceCollection
from main import dp


@dp.message(CommandStart(deep_link=True))
async def start_command_handler(message: Message, command: CommandObject) -> None:
    """
    Хендлер для команды /start

    :param message: aiogram Message
    :param command: Объект команды (нужен для реферальной системы
    :return: None
    """

    router = StartRouter(message, command)
    await router.route()



@dp.message(Command("search"))
async def search_command_handler(message: Message) -> None:
    """
    Хендлер команды /search

    :param message: aiogram.types.Message
    :return: None
    """

    router = SearchRouter(message)
    await router.route()


@dp.callback_query(ChoiceCollection.filter())
async def select_collection_handler(callback_query: CallbackQuery) -> None:
    """
    Хендлер для кнопок выбора коллекции, доступных после ввода /search

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """

    router =