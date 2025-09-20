from callbacks.profile_callbacks import ProfileAction
from localization_service.LocalesManager import LocalesManager
from localization_service.i18n import i18n
from localization_service.types import SystemMessages
from profile_service.keyboard_creators.SettingsKeyboardCreator import SettingsKeyboardCreator
from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter


class ProfileActionCallbackQueryRouter(BaseCallbackQueryRouter):
    async def route(self) -> None:
        callback_data = ProfileAction.unpack(self._callback_query.get_data())
        if callback_data.action == "settings":
            await self.__open_settings()

    async def __open_settings(self) -> None:
        """
        Открыть панель настроек

        :return: None
        """

        locale = await LocalesManager().get_locale(self._callback_query.get_from_user().get_id())

        text = i18n().get_text(SystemMessages.SETTINGS_MESSAGE, locale)
        reply_markup = SettingsKeyboardCreator(locale).get_keyboard()

        # Исправляем сообщение
        await self._callback_query.get_message().edit_message_text(text)
        await self._callback_query.get_message().edit_reply_markup(reply_markup)
