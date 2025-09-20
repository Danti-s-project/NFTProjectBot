from abstraction.keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from abstraction.keyboard.IInlineKeyboard import IInlineKeyboard
from callbacks.profile_callbacks import SettingsAction
from localization_service.types import SystemMessages
from localization_service.i18n import i18n


class SettingsKeyboardCreator:
    """
    Создать клавиатуру для настроект
    """

    def __init__(self, locale):
        self.__locale = locale

    def get_keyboard(self) -> IInlineKeyboard:
        reply_markup = InlineKeyboardFactory().create_keyboard()

        button = InlineKeyboardFactory().create_button()
        button.set_text(i18n().get_text(SystemMessages.LANGUAGE_BUTTON_TEXT, self.__locale))
        button.set_callback_data(SettingsAction(action="language").pack())

        reply_markup.add_button(button)

        return reply_markup
