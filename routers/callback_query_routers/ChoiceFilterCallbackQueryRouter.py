from aiogram.types import CallbackQuery

from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from search_nft_service.SearchStateManager import SearchStateManager
from search_nft_service.keyboard_creators.MainSearchMenuKeyboardMenu import MainSearchMenuKeyboardMenu
from callbacks.search_callbacks import ChoiceFilter

class ChoiceCollectionCallbackQueryRouter(BaseCallbackQueryRouter):

    def __init__(self, callback_query: CallbackQuery):
        super().__init__(callback_query)

    async def route(self) -> None:
        self.__write_filter_name()
        await self.__send_filters_message()

    def __write_filter_name(self) -> None:
        """
        Записываем название коллекции, которую ищет пользователь, в его статус

        :return: None
        """

        search_state = SearchStateManager().get(self.__callback_query.get_from_user().get_id())
        data = ChoiceFilter.unpack(self.__callback_query.get_data())

        match data.filter_type:
            case "model":
                search_state.model = data.filter_name
            case "backdrop":
                search_state.backdrop = data.filter_name
            case "symbol":
                search_state.symbol = data.filter_name


    async def __send_filters_message(self) -> None:
        """
        Отправить сообщение с клавиатурой в чат

        :return: None
        """

        search_state = SearchStateManager().get(self.__callback_query.get_from_user().get_id())
        keyboard = MainSearchMenuKeyboardMenu(
            model=search_state.model,
            backdrop=search_state.backdrop,
            symbol=search_state.symbol,
        ).get_keyboard()

        await self.__callback_query.get_message().answer(
            "Выставите фильтры:", reply_markup=keyboard)
