"""
Здесь все хендлеры команд бота
"""

from aiogram.filters.command import CommandStart, CommandObject,  Command
from aiogram.types import Message, CallbackQuery

from routers.message_routers.StartRouter import StartRouter
from routers.message_routers.SearchRouter import SearchRouter
from routers.callback_query_routers.ChoiceCollectionCallbackQueryRouter import ChoiceCollectionCallbackQueryRouter
from routers.callback_query_routers.ShowCollectionsPageCallbackQueryRouter import ShowCollectionsPageCallbackQueryRouter
from routers.callback_query_routers.SearchMenuActionCallbackQueryRouter import SearchMenuActionCallbackQueryRouter
from callbacks.search_callbacks import ChoiceCollection, ShowCollectionsPage
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

    router = ChoiceCollectionCallbackQueryRouter(callback_query)
    await router.route()


@dp.callback_query(ShowCollectionsPage.filter())
async def show_collections_page_callback_query_handler(callback_query: CallbackQuery) -> None:
    """
    Хендлер срабатывающий для кнопок пагинации по списку существующих коллекций

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """

    router = ShowCollectionsPageCallbackQueryRouter(callback_query)
    await router.route()


@dp.callback_query(ChoiceCollection.filter())
async def action_in_search_menu_callback_query_handler(callback_query: CallbackQuery) -> None:
    """
    Срабатывает при нажатии любой кнопки в главном меню поиска

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """
    router = SearchMenuActionCallbackQueryRouter(callback_query)
    await router.route()
