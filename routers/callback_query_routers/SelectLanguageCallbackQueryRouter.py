from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from api.APIService import APIService
from callbacks.profile_callbacks import SelectLanguage
from localization_service.LocalesManager import LocalesManager
from localization_service.i18n import i18n
from localization_service.types import SystemMessages


class SelectLanguageCallbackQueryRouter(BaseCallbackQueryRouter):
    async def route(self) -> None:
        callback_data = SelectLanguage.unpack(self._callback_query.get_data())

        # TODO: Добавить проверку на callback query

        await APIService().update_user(self._callback_query.get_from_user().get_id(), language=callback_data.language)

        # Обновляем язык в кеше LocalesManager'a
        LocalesManager().set_locale(self._callback_query.get_from_user().get_id(), callback_data.language)

        # Получаем локаль еще раз, так как set_locale принимает строку, а нам нужен объект типа Locale
        locale = await LocalesManager().get_locale(self._callback_query.get_from_user().get_id())

        # Отправляем сообщение об успешном изменении локали
        await self._callback_query.get_message().edit_message(
            text=i18n().get_text(SystemMessages.LANGUAGE_SUCCESSFUL_CHANGED, locale))
