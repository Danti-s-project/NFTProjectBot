from typing import Optional

from abstraction.keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from abstraction.keyboard.IInlineKeyboard import IInlineKeyboard
from abstraction.keyboard.IInlineButton import IInlineButton
from callbacks.search_callbacks import Action


class MainSearchMenuKeyboardMenu:
    """
    Креатор отвечающий за создание клавиатуры в главном меню сервиса /search
    """
    def __init__(self,
                 model: Optional[str] = None,
                 backdrop: Optional[str] = None,
                 symbol: Optional[str] = None
                 ):
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
            model_button.set_text(f"Модель: {self.__model}")
        else:
            model_button.set_text("Выбрать модель")
        model_button.set_callback_data(Action(action="model").pack())

        backdrop_button: IInlineButton = InlineKeyboardFactory.create_button()
        if self.__backdrop:
            backdrop_button.set_text(f"Фон: {self.__backdrop}")
        else:
            backdrop_button.set_text("Выбрать фон")
        backdrop_button.set_callback_data(Action(action="backdrop").pack())

        symbol_button: IInlineButton = InlineKeyboardFactory.create_button()
        if self.__symbol:
            symbol_button.set_text(f"Символ: {self.__symbol}")
        else:
            symbol_button.set_text("Выбрать символ")
        symbol_button.set_callback_data(Action(action="symbol").pack())

        search_button: IInlineButton = InlineKeyboardFactory.create_button()
        search_button.set_text("Поиск")
        search_button.set_callback_data(Action(action="search").pack())

        self.__keyboard.add_buttons_row([model_button, backdrop_button, symbol_button])
        self.__keyboard.add_buttons_row([search_button])

        return self.__keyboard
