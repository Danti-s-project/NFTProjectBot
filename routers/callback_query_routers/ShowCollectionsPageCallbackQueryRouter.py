from typing import List

from localization_service import LocalesManager
from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from search_nft_service.keyboard_creators.CollectionChoiceKeyboardCreator import CollectionChoiceKeyboardCreator
from search_nft_service.SearchStateManager import SearchStateManager
from api.APIService import APIService
from api.models import Collection
from callbacks.search_callbacks import ShowCollectionsPage

class ShowCollectionsPageCallbackQueryRouter(BaseCallbackQueryRouter):
    async def route(self) -> None:

        # Распаковываем callback data
        callback_data: ShowCollectionsPage = ShowCollectionsPage.unpack(self._callback_query.get_data())

        # Получаем ссылку на пагинацию коллекций
        search_state = SearchStateManager().get(self._callback_query.get_from_user().get_id())
        if callback_data.direction == "next":
            url = search_state.next_page
        else:
            url = search_state.previous_page

        # делаем запрос и крафтим клавиатуру
        data = await self.__get_page(url)
        keyboard = CollectionChoiceKeyboardCreator(
            data,
            await LocalesManager().get_locale(self._callback_query.get_from_user().get_id()),
            next_page=search_state.next_page,
            previous_page=search_state.previous_page
        ).get_keyboard()

        # Отправляем сообщение
        await self._callback_query.get_message().edit_reply_markup(reply_markup=keyboard)

    async def __get_page(self, url: str) -> List[Collection]:
        """
        Получить следующую страницу с коллекциями

        :param url: ссылка на следующую пагинацию
        :return: лист с коллекциями
        """

        response = await APIService().get_collections(url)

        search_state = SearchStateManager().get(self._callback_query.get_from_user().get_id())

        search_state.next_page = response.next
        search_state.previous_page = response.previous

        return response.results
