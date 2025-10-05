from functools import lru_cache

from abstraction.inline_keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from abstraction.inline_keyboard.IInlineKeyboard import IInlineKeyboard
from callbacks.profile_callbacks import SettingsAction
from localization_service import SystemMessages, i18n


class SettingsKeyboardCreator:
    """
    Создать клавиатуру для настроек
    Singleton
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(SettingsKeyboardCreator, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True
            self.__init(*args, **kwargs)

    def __init(self, locale):
        self.__locale = locale

    @lru_cache(8)
    def __create_keyboard(self, locale) -> IInlineKeyboard:
        """
        Возвращает созданный объект клавиатуры
        Т.к. количество локалей можно пересчитать по пальцам, завернул в LRU для оптимизации

        :param locale: язык
        :return: клавиатура
        """
        reply_markup = InlineKeyboardFactory().create_keyboard()

        button = InlineKeyboardFactory().create_button()
        button.set_text(i18n().get_text(SystemMessages.LANGUAGE_BUTTON_TEXT, locale))
        button.set_callback_data(SettingsAction(action="language").pack())

        reply_markup.add_button(button)

        return reply_markup

    def get_keyboard(self) -> IInlineKeyboard:
        """
        Получите клавиатуру
        :return: объект клавиатуры
        """

        return self.__create_keyboard(self.__locale)
