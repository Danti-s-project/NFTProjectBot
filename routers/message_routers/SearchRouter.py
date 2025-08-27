import os
from typing import List

from aiogram.types import Message
import aiohttp

from abstraction.keyboard.IInlineKeyboard import IInlineKeyboard
from abstraction.keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from routers.message_routers.BaseMessageRouter import BaseMessageRouter
from search_nft_service.SearchStateManager import SearchStateManager
from search_nft_service.keyboard_creators.CollectionChoiceKeyboardCreator import CollectionChoiceKeyboardCreator


class SearchRouter(BaseMessageRouter):
    """
    Роутер для команды /search
    """

    HOST = os.getenv("HOST")
    COLLECTIONS_PATH = "api/v1/collections/"
    ELEMENTS_IN_PAGE = 2

    def __init__(self, message: Message):
        super().__init__(message)

    async def route(self) -> None:
        user_id = self.__message.get_from_user().get_id()

        SearchStateManager().remove(user_id)
        SearchStateManager().create(user_id)

    async def __send_search_message(self) -> None:
        """
        Отправить сообщение с поиском
        :return:
        """

        reply_markup = self.__create_keyboard()
        await self.__message.answer(
            "Выбери коллекцию подарков которая будет рассматриваться",
            reply_markup=reply_markup)

    async def __create_keyboard(self) -> IInlineKeyboard:
        """
        Создаем клавиатуру для сообщения с коллекциями
        :return:
        """

        # Запрашиваем коллекции с сервера
        nft_collections = await self.__request_first_page()
        next_page = SearchStateManager().get(self.__message.get_from_user().get_id()).next_page

        keyboard = CollectionChoiceKeyboardCreator(
            nft_collections,
            next_page=next_page
        ).get_keyboard()

        return keyboard

    async def __request_first_page(self) -> List[dict]:
        """
        Запрос к списку коллекций

        :return:
        """
        async with (aiohttp.ClientSession() as session):
            async with session.get(
                    f"{SearchRouter.HOST}{SearchRouter}?limit={SearchRouter.ELEMENTS_IN_PAGE}&offset=0"
            ) as response:
                response_json = await response.json()

                search_state = SearchStateManager().get(self.__message.get_from_user().get_id())
                search_state.next_page = response_json

                return response_json["result"]
