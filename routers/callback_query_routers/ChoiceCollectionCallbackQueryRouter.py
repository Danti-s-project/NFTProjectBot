from aiogram.types import CallbackQuery

from callbacks.search_callbacks import ChoiceCollection
from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from search_nft_service.SearchStateManager import SearchStateManager
from search_nft_service.keyboard_creators.MainSearchMenuKeyboardMenu import MainSearchMenuKeyboardMenu

class ChoiceCollectionCallbackQueryRouter(BaseCallbackQueryRouter):

    def __init__(self, callback_query: CallbackQuery):
        super().__init__(callback_query)

    async def route(self) -> None:
        self.__write_collection_name()
        await self.__send_filters_message()

    def __write_collection_name(self) -> None:
        """
        Записываем название коллекции, которую ищет пользователь, в его статус

        :return: None
        """

        data = ChoiceCollection.unpack(self._callback_query.get_data())
        SearchStateManager().get(
            self._callback_query.get_from_user().get_id()
        ).collection_name = data.collection_name

    async def __send_filters_message(self) -> None:
        """
        Отправить сообщение с клавиатурой в чат

        :return: None
        """
        keyboard = MainSearchMenuKeyboardMenu().get_keyboard()
        await self._callback_query.get_message().answer(
            "Выставите фильтры:", reply_markup=keyboard)
