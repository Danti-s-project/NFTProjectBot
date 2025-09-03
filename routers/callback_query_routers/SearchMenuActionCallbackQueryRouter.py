import os

from abstraction.IMessage import IMessageAdapter
from abstraction.keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from api.APIService import APIService
from api.models import NFTSAPIResponse, PaginationAPIReponse, Symbol, Model, Backdrop
from callbacks.search_callbacks import Action, Back
from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from search_nft_service.SearchStateManager import SearchStateManager
from search_nft_service.keyboard_creators.FiltersChoiceKeyboardCreate import FiltersChoiceKeyboardCreator
from localization_service.LocalesManager import LanguageManager
from localization_service.types import SystemMessages, Locale
from localization_service.i18n import i18n


class SearchMenuActionCallbackQueryRouter(BaseCallbackQueryRouter):
    """
    Роутер обрабатывающий все нажатия в главном меню /search
    """

    HOST = os.getenv("HOST")
    PAGE_LIMIT = 2

    async def route(self) -> None:
        data = Action.unpack(self._callback_query.get_data())

        match data.action:
            case "search":
                await self.__search_menu_action()
            case "model":
                await self.__model_menu_action()
            case "backdrop":
                await self.__backdrop_menu_action()
            case "symbol":
                await self.__symbol_menu_action()

    async def __search_menu_action(self) -> None:
        """
        Выполняет действия после нажатия кнопки поиск

        :return: None
        """

        search_state = SearchStateManager().get(self._callback_query.get_from_user().get_id())

        result: NFTSAPIResponse = await APIService().get_nfts(
            search_state.collection,
            model=search_state.model,
            backdrop=search_state.backdrop,
            symbol=search_state.symbol
        )

        locale = await LanguageManager().get_locale(self._callback_query.get_from_user().get_id())

        message = i18n().get_text(
            SystemMessages.SEARCH_RESULT_HEADER_TEXT,
            locale,
            len(result.result), search_state.collection.name
        )

        if search_state.model:
            message += f"{i18n().get_text(
                SystemMessages.SEARCH_RESULT_MODEL_TEXT,
                locale,
                search_state.model)}\n"

        if search_state.backdrop:
            message += f"{i18n().get_text(
                SystemMessages.SEARCH_RESULT_BACKDROP_TEXT,
                locale,
                search_state.backdrop)}\n"

        if search_state.symbol:
            message += f"{i18n().get_text(
                SystemMessages.SEARCH_RESULT_SYMBOL_TEXT,
                locale,
                search_state.symbol)}\n"

        message += "\n\n"

        for item in result.result:
            message += \
                (f"{item.collection.name}:\n"
                 f"{i18n().get_text(
                SystemMessages.SEARCH_RESULT_MODEL_TEXT,
                locale,
                item.model)}\n"
                 
                 f"{i18n().get_text(
                SystemMessages.SEARCH_RESULT_SYMBOL_TEXT,
                locale,
                item.symbol)}\n"
                 
                 f"{i18n().get_text(
                SystemMessages.SEARCH_RESULT_BACKDROP_TEXT,
                locale,
                item.backdrop)}\n"
                 )

            if item.owner:
                message += f"{i18n().get_text(SystemMessages.SEARCH_RESULT_OWNER_TEXT, locale, item.owner.name)}\n"

            message += "\n\n"


        # Создаем клавиатуру для сообщения

        keyboard = InlineKeyboardFactory.create_keyboard()

        back_button = InlineKeyboardFactory.create_button()

        # Получаем текст кнопки
        button_text = i18n().get_text(SystemMessages.BACK_BUTTON_TEXT, locale)
        back_button.set_text(button_text)
        back_button.set_callback_data(Back().pack())
        keyboard.add_buttons_row([back_button])

        await self._callback_query.get_message().edit_message_text(message)
        await self._callback_query.get_message().edit_reply_markup(reply_markup=keyboard)

    async def __model_menu_action(self) -> None:
        """
        Выполняет действия после нажатия кнопки модель

        :return: None
        """

        locale: Locale = await LanguageManager().get_locale(self._callback_query.get_from_user().get_id())

        # Получаем нужные данные для формирования сообщений
        search_state = SearchStateManager().get(self._callback_query.get_from_user().get_id())
        data: PaginationAPIReponse[Model] = await APIService().get_models(
            f"{SearchMenuActionCallbackQueryRouter.HOST}"
            f"/api/v1/nfts/models/?offset=0&limit={SearchMenuActionCallbackQueryRouter.PAGE_LIMIT}")
        search_state.next_page = data.next

        # Редактируем клавиатуру
        keyboard = FiltersChoiceKeyboardCreator(data, data.next, locale).get_keyboard()
        message: IMessageAdapter = self._callback_query.get_message()
        await message.edit_reply_markup(reply_markup=keyboard)

        # Получаем текст сообщения
        message_text = i18n().get_text(SystemMessages.SELECT_MODEL_MESSAGE, locale)
        await message.edit_message_text(message_text)

    async def __backdrop_menu_action(self) -> None:
        """
        Выполняет действия после нажатия кнопки фон

        :return: None
        """

        locale: Locale = await LanguageManager().get_locale(self._callback_query.get_from_user().get_id())

        search_state = SearchStateManager().get(self._callback_query.get_from_user().get_id())
        data: PaginationAPIReponse[Backdrop] = await APIService().get_backdrops(
            f"{SearchMenuActionCallbackQueryRouter.HOST}"
            f"/api/v1/nfts/backdropss/?offset=0&limit={SearchMenuActionCallbackQueryRouter.PAGE_LIMIT}")
        search_state.next_page = data.next

        keyboard = FiltersChoiceKeyboardCreator(data, data.next, locale).get_keyboard()

        message: IMessageAdapter = self._callback_query.get_message()
        await message.edit_reply_markup(reply_markup=keyboard)

        # Изменяем сообщение
        message_text = i18n().get_text(SystemMessages.SELECT_BACKDROP_MESSAGE, locale)
        await message.edit_message_text(message_text)

    async def __symbol_menu_action(self) -> None:
        """
        Выполняет действия после нажатия кнопки символ

        :return: None
        """

        search_state = SearchStateManager().get(self._callback_query.get_from_user().get_id())
        data: PaginationAPIReponse[Symbol] = await APIService().get_symbols(
            f"{SearchMenuActionCallbackQueryRouter.HOST}"
            f"/api/v1/nfts/symbols/?offset=0&limit={SearchMenuActionCallbackQueryRouter.PAGE_LIMIT}")

        search_state.next_page = data.next

        locale: Locale = await LanguageManager().get_locale(self._callback_query.get_from_user().get_id())

        keyboard = FiltersChoiceKeyboardCreator(data, data.next, locale).get_keyboard()

        message: IMessageAdapter = self._callback_query.get_message()
        await message.edit_reply_markup(reply_markup=keyboard)

        # Изменяем сообщение
        message_text = i18n().get_text(SystemMessages.SELECT_SYMBOL_MESSAGE, locale)
        await message.edit_message_text(message_text)
