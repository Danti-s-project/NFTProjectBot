from api.APIService import APIService
from api.models import BaseNFTDataclass, PaginationAPIReponse
from callbacks.search_callbacks import ShowFilterPage
from localization_service.LocalesManager import LanguageManager
from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from search_nft_service.SearchStateManager import SearchStateManager
from search_nft_service.keyboard_creators.FiltersChoiceKeyboardCreate import FiltersChoiceKeyboardCreator


class ShowFilterPageCallbackQueryRouter(BaseCallbackQueryRouter):
    async def route(self) -> None:

        # Распаковываем callback data
        callback_data: ShowFilterPage = ShowFilterPage.unpack(self._callback_query.get_data())

        # Получаем ссылку на пагинацию коллекций
        search_state = SearchStateManager().get(self._callback_query.get_from_user().get_id())
        if callback_data.direction == "next":
            url = search_state.next_page
        else:
            url = search_state.previous_page

        # делаем запрос и крафтим клавиатуру
        data = await self.__get_page(url)
        keyboard = FiltersChoiceKeyboardCreator(
            data,
            callback_data.filter_type,
            await LanguageManager().get_locale(self._callback_query.get_from_user().get_id()),
            next_page=search_state.next_page,
            previous_page=search_state.previous_page
        ).get_keyboard()

        # Отправляем сообщение
        await self._callback_query.get_message().edit_reply_markup(reply_markup=keyboard)

    async def __get_page(self, url: str) -> PaginationAPIReponse:
        """
        Получить следующую страницу с коллекциями

        :param url: ссылка на следующую пагинацию
        :return: лист с коллекциями
        """

        response = await APIService().endpoint_with_pagination_request(url, BaseNFTDataclass)

        search_state = SearchStateManager().get(self._callback_query.get_from_user().get_id())

        search_state.next_page = response.next
        search_state.previous_page = response.previous

        return response
