from abstraction.keyboard.IInlineKeyboard import IInlineKeyboard
from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from search_nft_service.keyboard_creators.MainSearchMenuKeyboardMenu import MainSearchMenuKeyboardMenu
from search_nft_service.SearchStateManager import SearchStateManager


class SearchMenuBackButtonCallbackQueryRouter(BaseCallbackQueryRouter):
    """
    Роутер обрабатывающий клики на кнопки back в /search
    """

    async def route(self) -> None:
        keyboard = MainSearchMenuKeyboardMenu().get_keyboard()
        await self.__callback_query.get_message().edit_reply_markup(reply_markup=keyboard)
        await self.__callback_query.get_message().edit_message_text("Выставите фильтры:")

    def __create_keyboard(self) -> IInlineKeyboard:
        """
        Получить клавиатуру

        :return: клавиатура для сообщения
        """

        search_state = SearchStateManager().get(self.__callback_query.get_from_user().get_id())
        keyboard = MainSearchMenuKeyboardMenu(
            model=search_state.model,
            backdrop=search_state.backdrop,
            symbol=search_state.symbol
        ).get_keyboard()

        return keyboard

