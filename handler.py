"""
Здесь все хендлеры команд бота
"""

import logging

from aiogram.filters.command import CommandStart, CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from callbacks.courses_callback import SelectCourse, SelectChapter, SelectLesson
from callbacks.profile_callbacks import ProfileAction, SettingsAction, SelectLanguage
from callbacks.search_callbacks import ChoiceCollection, ShowCollectionsPage, Back, Action, ChoiceFilter
from dispatcher import dp
from routers.Middleware.MainMiddleware import MainMiddleware
from fsm.course_fsm.CourseStateGroup import CourseStateGroup
from routers.callback_query_routers.ChoiceCollectionCallbackQueryRouter import ChoiceCollectionCallbackQueryRouter
from routers.callback_query_routers.ChoiceFilterCallbackQueryRouter import ChoiceFilterCallbackQueryRouter
from routers.callback_query_routers.ProfileActoinCallbackQueryRouter import ProfileActionCallbackQueryRouter
from routers.callback_query_routers.SearchMenuActionCallbackQueryRouter import SearchMenuActionCallbackQueryRouter
from routers.callback_query_routers.SearchMenuBackButtonCallbackQueryRouter import \
    SearchMenuBackButtonCallbackQueryRouter
from routers.callback_query_routers.SelectChapterCallbackQueryRouter import SelectChapterCallbackQueryRouter
from routers.callback_query_routers.SelectCourseCallbackQueryRouter import SelectCourseCallbackQueryRouter
from routers.callback_query_routers.SelectLanguageCallbackQueryRouter import SelectLanguageCallbackQueryRouter
from routers.callback_query_routers.SelectLessonCallbackQueryRouter import SelectLessonCallbackQueryRouter
from routers.callback_query_routers.SettingsActionCallbackQueryRouter import SettingsActionCallbackQueryRouter
from routers.callback_query_routers.ShowCollectionsPageCallbackQueryRouter import ShowCollectionsPageCallbackQueryRouter
from routers.fsm_routers.CourseFSMRouter import CourseFSMRouter
from routers.message_routers.CourseCommandRouter import CourseCommandRouter
from routers.message_routers.ProfileRouter import ProfileRouter
from routers.message_routers.SearchRouter import SearchRouter
from routers.message_routers.StartRouter import StartRouter
from routers.message_routers.StartRouterWithDeeplLnk import StartRouterWithDeepLink

logger = logging.getLogger('handler')


@dp.message(CommandStart(deep_link=True))
async def start_command_with_deeplink_handler(message: Message, command: CommandObject) -> None:
    """
    Хендлер для команды /start с реферальной ссылкой

    :param message: aiogram Message
    :param command: Объект команды (нужен для реферальной системы
    :return: None
    """
    logger.info(f"Пользователь {message.from_user.id} использовал команду /start c deep link")

    router = StartRouterWithDeepLink(message, command)
    await router.route()


@dp.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    """
    Хэндлер для команды /start без реферальной ссылки

    :param message: aiogram Message
    :return: None
    """

    logger.info(f"Пользователь {message.from_user.id} использовал команду /start")

    router = StartRouter(message)
    await router.route()



@dp.message(Command("search"))
async def search_command_handler(message: Message) -> None:
    """
    Хендлер команды /search

    :param message: aiogram.types.Message
    :return: None
    """
    logger.info(f"Пользователь {message.from_user.id} использовал команду /search")

    router = SearchRouter(message)
    await router.route()


@dp.callback_query(ChoiceCollection.filter())
async def select_collection_handler(callback_query: CallbackQuery) -> None:
    """
    Хендлер для кнопок выбора коллекции, доступных после ввода /search

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """

    logger.info(f"Пользователь {callback_query.from_user.id} выбрал коллекцию в /search")

    router = ChoiceCollectionCallbackQueryRouter(callback_query)
    await router.route()


@dp.callback_query(ShowCollectionsPage.filter())
async def show_collections_page_callback_query_handler(callback_query: CallbackQuery) -> None:
    """
    Хендлер срабатывающий для кнопок пагинации по списку существующих коллекций

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """

    logger.info(f"Пользователь {callback_query.from_user.id} листает список коллекций в /search")

    router = ShowCollectionsPageCallbackQueryRouter(callback_query)
    await router.route()


@dp.callback_query(Action.filter())
async def action_in_search_menu_callback_query_handler(callback_query: CallbackQuery) -> None:
    """
    Срабатывает при нажатии любой кнопки в главном меню поиска

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """

    logger.info(f"Пользователь {callback_query.from_user.id} нажал кнопку в главном меню /search")

    router = SearchMenuActionCallbackQueryRouter(callback_query)
    await router.route()


@dp.callback_query(Back.filter())
async def search_menu_back_button_callback_query_handler(callback_query: CallbackQuery) -> None:
    """
    Срабатывает при нажатии кнопки назад в подменю сервиса /search

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """

    logger.info(f"Пользователь {callback_query.from_user.id} нажал кнопку назад в /search меню")

    router = SearchMenuBackButtonCallbackQueryRouter(callback_query)
    await router.route()



@dp.callback_query(ChoiceFilter.filter())
async def choice_filter_button_callback_query_handler(callback_query: CallbackQuery) -> None:
    """
    Срабатывает при нажатии кнопки выбора фильтра в сервисе /search

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """

    logger.info(f"Пользователь {callback_query.from_user.id} нажал кнопку выбора одного из фильтров в /search меню")

    router = ChoiceFilterCallbackQueryRouter(callback_query)
    await router.route()


@dp.message(Command("profile"))
async def profile_command_handler(message: Message) -> None:
    """
    Хэндлер для команды /profile

    :param message: aiogram Message
    :return: None
    """

    logger.info(f"Пользователь {message.from_user.id} использовал команду /profile")

    router = ProfileRouter(message)
    await router.route()


@dp.callback_query(ProfileAction.filter())
async def profile_action_callback_query_handler(callback_query: CallbackQuery) -> None:
    """
    Срабатывает при нажатии кнопки в главном меню profile

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """

    logger.info(f"Пользователь {callback_query.from_user.id} нажал кнопку в меню /profile")

    router = ProfileActionCallbackQueryRouter(callback_query)
    await router.route()


@dp.callback_query(SettingsAction.filter())
async def settings_action_callback_query_handler(callback_query: CallbackQuery) -> None:
    """
    Срабатывает при нажатии кнопки в главном меню настроек

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """

    logger.info(f"Пользователь {callback_query.from_user.id} нажал кнопку в меню настроек")

    router = SettingsActionCallbackQueryRouter(callback_query)
    await router.route()


@dp.callback_query(SelectLanguage.filter())
async def select_language_callback_query_handler(callback_query: CallbackQuery) -> None:
    """
    Срабатывает при нажатии кнопки в меню выбора языка

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """

    logger.info(f"Пользователь {callback_query.from_user.id} нажал кнопку в меню выбора языка")

    router = SelectLanguageCallbackQueryRouter(callback_query)
    await router.route()


@dp.message(Command("course"))
async def course_command_handler(message: Message) -> None:
    """
    Срабатывает при использовании команды /course

    :param message: aiogram.types.Message
    :return: None
    """

    logger.info(f"Пользователь {message.from_user.id} использовал команду /course")

    router = CourseCommandRouter(message)
    await router.route()


@dp.callback_query(SelectCourse.filter())
async def select_course_callback_query_handler(callback_query: CallbackQuery) -> None:
    """
    Срабатывает при выборе курса в /course

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """

    logger.info(f"Пользователь {callback_query.from_user.id} нажал кнопку выбора курсов в /course")

    router = SelectCourseCallbackQueryRouter(callback_query)
    await router.route()


@dp.callback_query(SelectChapter.filter())
async def select_chapter_callback_query_query_handler(callback_query: CallbackQuery) -> None:
    """
    Срабатывает при выборе главы в /course

    :param callback_query: aiogram.types.CallbackQuery
    :return: None
    """

    logger.info(f"Пользователь {callback_query.from_user.id} нажал кнопку выбора главы в /course")

    router = SelectChapterCallbackQueryRouter(callback_query)
    await router.route()


@dp.callback_query(SelectLesson.filter())
async def select_lesson_callback_query_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Срабатывает при выборе урока в /course

    :param callback_query: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """

    logger.info(f"Пользователь {callback_query.from_user.id} нажал кнопку выбора урока в /course")

    router = SelectLessonCallbackQueryRouter(callback_query, fsm_state=state)
    await router.route()


@dp.message(CourseStateGroup.lesson)
async def lesson_fsm_handler(message: Message, state: FSMContext) -> None:
    """
    Срабатывает при нажатии кнопки прохождения урока

    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """

    logger.info(f"Пользователь {message.from_user.id} проходит уроки")

    router = CourseFSMRouter(message, state)
    await router.route()


dp.message.middleware(MainMiddleware())
dp.callback_query.middleware(MainMiddleware())
