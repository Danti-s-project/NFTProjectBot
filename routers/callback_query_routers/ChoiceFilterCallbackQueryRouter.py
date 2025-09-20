from aiogram.types import CallbackQuery

from api.models import Backdrop, Symbol, Model
from callbacks.search_callbacks import ChoiceFilter
from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from search_nft_service.SearchStateManager import SearchStateManager
from search_nft_service.keyboard_creators.MainSearchMenuKeyboardMenu import MainSearchMenuKeyboardMenu
from localization_service.LocalesManager import LocalesManager
from localization_service.types import SystemMessages, Locale
from localization_service.i18n import i18n


class ChoiceFilterCallbackQueryRouter(BaseCallbackQueryRouter):

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

        search_state = SearchStateManager().get(self._callback_query.get_from_user().get_id())
        data = ChoiceFilter.unpack(self._callback_query.get_data())

        match data.filter_type:
            case "model":
                search_state.model = Model(name=data.filter_name)
            case "backdrop":
                search_state.backdrop = Backdrop(name=data.filter_name)
            case "symbol":
                search_state.symbol = Symbol(name=data.filter_name)


    async def __send_filters_message(self) -> None:
        """
        Отправить сообщение с клавиатурой в чат

        :return: None
        """

        locale: Locale = await LocalesManager().get_locale(self._callback_query.get_from_user().get_id())

        # Создаем клавиатуру
        search_state = SearchStateManager().get(self._callback_query.get_from_user().get_id())
        keyboard = MainSearchMenuKeyboardMenu(
            locale,
            model=search_state.model,
            backdrop=search_state.backdrop,
            symbol=search_state.symbol,
        ).get_keyboard()

        # Получаем текст сообщения
        message = i18n().get_text(SystemMessages.SET_FILTERS_MESSAGE, locale)

        # Отправляем
        await self._callback_query.get_message().answer(message, reply_markup=keyboard)
