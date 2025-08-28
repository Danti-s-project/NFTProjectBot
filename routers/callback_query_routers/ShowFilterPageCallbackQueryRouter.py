import aiohttp

from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from search_nft_service.keyboard_creators.FiltersChoiceKeyboardCreate import FiltersChoiceKeyboardCreator
from callbacks.search_callbacks import ShowFilterPage
from search_nft_service.SearchStateManager import SearchStateManager

class ShowFilterPageCallbackQueryRouter(BaseCallbackQueryRouter):
    async def route(self) -> None:

        # Распаковываем callback data
        callback_data: ShowFilterPage = ShowFilterPage.unpack(self.__callback_query.get_data())

        # Получаем ссылку на пагинацию коллекций
        search_state = SearchStateManager().get(self.__callback_query.get_from_user().get_id())
        if callback_data.direction == "next":
            url = search_state.next_page
        else:
            url = search_state.previous_page

        # делаем запрос и крафтим клавиатуру
        data = await self.__get_page(url)
        keyboard = FiltersChoiceKeyboardCreator(
            data,
            callback_data.filter_type,
            next_page=search_state.next_page,
            previous_page=search_state.previous_page
        ).get_keyboard()

        # Отправляем сообщение
        await self.__callback_query.get_message().edit_reply_markup(reply_markup=keyboard)

    async def __get_page(self, url: str) -> list:
        """
        Получить следующую страницу с коллекциями

        :param url: ссылка на следующую пагинацию
        :return: лист с коллекциями
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_json =  await response.json()

                search_state = SearchStateManager().get(self.__callback_query.get_from_user().get_id())

                search_state.next_page = response_json["next"]
                search_state.previous_page = response_json["previous"]

                return response_json["result"]
