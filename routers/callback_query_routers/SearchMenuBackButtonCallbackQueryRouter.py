from abstraction.inline_keyboard.IInlineKeyboard import IInlineKeyboard
from localization_service.LocalesManager import LocalesManager
from localization_service.i18n import i18n
from localization_service.types import SystemMessages, Locale
from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from search_nft_service.keyboard_creators.MainSearchMenuKeyboardMenu import MainSearchMenuKeyboardMenu
from search_nft_service.SearchStateManager import SearchStateManager


class SearchMenuBackButtonCallbackQueryRouter(BaseCallbackQueryRouter):
    """
    Роутер обрабатывающий клики на кнопки back в /search
    """

    async def route(self) -> None:

        locale = await LocalesManager().get_locale(self._callback_query.get_from_user().get_id())

        keyboard = MainSearchMenuKeyboardMenu(locale).get_keyboard()
        await self._callback_query.get_message().edit_reply_markup(reply_markup=keyboard)
        await self._callback_query.get_message().edit_message_text(i18n().get_text(SystemMessages.SET_FILTERS_MESSAGE, locale))
