import os
from typing import List

from aiogram.types import Message

from api.APIService import APIService
from api.models import Collection
from abstraction.inline_keyboard.IInlineKeyboard import IInlineKeyboard
from routers.message_routers.BaseMessageRouter import BaseMessageRouter
from search_nft_service.SearchStateManager import SearchStateManager
from search_nft_service.keyboard_creators.CollectionChoiceKeyboardCreator import CollectionChoiceKeyboardCreator
from localization_service.LocalesManager import LocalesManager
from localization_service.types import SystemMessages, Locale
from localization_service.i18n import i18n


class SearchRouter(BaseMessageRouter):
    """
    Роутер для команды /search
    """

    HOST = os.getenv("HOST")
    COLLECTIONS_PATH = "/api/v1/collections/"
    ELEMENTS_IN_PAGE = 2

    def __init__(self, message: Message):
        super().__init__(message)

    async def route(self) -> None:
        user_id = self._message.get_from_user().get_id()

        # Удалить пользователя если он существует, иначе ничего не произойдет
        SearchStateManager().remove(user_id)
        SearchStateManager().create(user_id)

        await self.__send_search_message()

    async def __send_search_message(self) -> None:
        """
        Отправить сообщение с поиском
        :return:
        """

        reply_markup = await self.__create_keyboard()

        locale = await LocalesManager().get_locale(self._message.get_from_user().get_id())
        message_text = i18n().get_text(SystemMessages.SELECT_COLLECTION_MESSAGE, locale)

        await self._message.answer(message_text, reply_markup=reply_markup)

    async def __create_keyboard(self) -> IInlineKeyboard:
        """
        Создаем клавиатуру для сообщения с коллекциями
        :return:
        """

        # Запрашиваем коллекции с сервера
        nft_collections = await self.__request_first_page()
        next_page = SearchStateManager().get(self._message.get_from_user().get_id()).next_page

        keyboard = CollectionChoiceKeyboardCreator(
            nft_collections,
            await LocalesManager().get_locale(self._message.get_from_user().get_id()),
            next_page=next_page
        ).get_keyboard()

        return keyboard

    async def __request_first_page(self) -> List[Collection]:
        """
        Запрос к списку коллекций

        :return:
        """
        response = await APIService().get_collections(
            f"{SearchRouter.HOST}{SearchRouter.COLLECTIONS_PATH}?limit={SearchRouter.ELEMENTS_IN_PAGE}&offset=0"
        )
        search_state = SearchStateManager().get(self._message.get_from_user().get_id())
        search_state.next_page = response.next

        return response.result
