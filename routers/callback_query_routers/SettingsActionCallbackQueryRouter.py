from abstraction.inline_keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from callbacks.profile_callbacks import SettingsAction, SelectLanguage
from localization_service import i18n, SystemMessages, LocalesManager


class SettingsActionCallbackQueryRouter(BaseCallbackQueryRouter):
    async def route(self) -> None:
        data = SettingsAction.unpack(self._callback_query.get_data())

        if data.action == "language":
            await self.__send_language_message()

    async def __send_language_message(self) -> None:
        locale = await LocalesManager().get_locale(self._callback_query.get_from_user().get_id())

        text = i18n().get_text(SystemMessages.PLEASE_SELECT_LANGUAGE_TEXT, locale)

        # Формируем клавиатуру
        reply_markup = InlineKeyboardFactory().create_keyboard()

        english_button = InlineKeyboardFactory().create_button()
        english_button.set_text("English")
        english_button.set_callback_data(SelectLanguage(language="en").pack())
        english_row = reply_markup.add_row()
        english_row.add_button(english_button)

        russian_button = InlineKeyboardFactory().create_button()
        russian_button.set_text("Русский")
        russian_button.set_callback_data(SelectLanguage(language="ru").pack())
        russian_row = reply_markup.add_row()
        russian_row.add_button(russian_button)

        chinese_button = InlineKeyboardFactory().create_button()
        chinese_button.set_text("中文")
        chinese_button.set_callback_data(SelectLanguage(language="zh").pack())
        chinese_row = reply_markup.add_row()
        chinese_row.add_button(chinese_button)


        await self._callback_query.get_message().edit_message(text, reply_markup=reply_markup)
