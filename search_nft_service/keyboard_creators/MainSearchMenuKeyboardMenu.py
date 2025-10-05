from typing import Optional

from abstraction.inline_keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from abstraction.inline_keyboard.IInlineKeyboard import IInlineKeyboard
from abstraction.inline_keyboard.IInlineButton import IInlineButton
from callbacks.search_callbacks import Action
from localization_service import SystemMessages, Locale, i18n


class MainSearchMenuKeyboardMenu:
    """
    Креатор отвечающий за создание клавиатуры в главном меню сервиса /search
    """

    def __init__(self,
                 locale: Locale,
                 model: Optional[str] = None,
                 backdrop: Optional[str] = None,
                 symbol: Optional[str] = None
                 ):

        self.__locale = locale
        self.__model = model
        self.__backdrop = backdrop
        self.__symbol = symbol
        self.__keyboard: IInlineKeyboard = InlineKeyboardFactory.create_keyboard()

    def get_keyboard(self) -> IInlineKeyboard:
        """
        Создать клавиатуру главного меню
        :return:
        """

        model_button: IInlineButton = InlineKeyboardFactory.create_button()
        if self.__model:
            model_button.set_text(i18n().get_text(
                SystemMessages.SELECT_MODEL_EXISTS_BUTTON_TEXT,
                self.__locale,
                self.__model))
        else:
            model_button.set_text(i18n().get_text(SystemMessages.SELECT_MODEL_BUTTON_TEXT, self.__locale))
        model_button.set_callback_data(Action(action="model").pack())

        backdrop_button: IInlineButton = InlineKeyboardFactory.create_button()
        if self.__backdrop:
            backdrop_button.set_text(
                i18n().get_text(
                SystemMessages.SELECT_BACKDROP_EXISTS_BUTTON_TEXT,
                self.__locale,
                self.__backdrop))
        else:
            backdrop_button.set_text(i18n().get_text(SystemMessages.SELECT_BACKDROP_BUTTON_TEXT, self.__locale))
        backdrop_button.set_callback_data(Action(action="backdrop").pack())

        symbol_button: IInlineButton = InlineKeyboardFactory.create_button()
        if self.__symbol:
            symbol_button.set_text(i18n().get_text(
                SystemMessages.SELECT_SYMBOL_EXISTS_BUTTON_TEXT,
                self.__locale,
                self.__symbol))
        else:
            symbol_button.set_text(i18n().get_text(SystemMessages.SELECT_SYMBOL_BUTTON_TEXT, self.__locale))
        symbol_button.set_callback_data(Action(action="symbol").pack())

        search_button: IInlineButton = InlineKeyboardFactory.create_button()
        search_button.set_text(i18n().get_text(SystemMessages.SEARCH_BUTTON_TEXT, self.__locale))
        search_button.set_callback_data(Action(action="search").pack())

        self.__keyboard.add_buttons_row([model_button, backdrop_button, symbol_button])
        self.__keyboard.add_buttons_row([search_button])

        return self.__keyboard
