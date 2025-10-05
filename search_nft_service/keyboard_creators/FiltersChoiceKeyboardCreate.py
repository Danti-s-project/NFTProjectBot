from typing import Optional

from abstraction.inline_keyboard.IInlineKeyboard import IInlineKeyboard
from abstraction.inline_keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from api.models import PaginationAPIReponse, BaseNFTDataclass
from callbacks.search_callbacks import ShowFilterPage, ChoiceFilter, Back
from localization_service import i18n, Locale, SystemMessages


class FiltersChoiceKeyboardCreator:
    """
    Создать клавиатуру для фильтров
    """

    ROW_SIZE = 2

    def __init__(self, items: PaginationAPIReponse[BaseNFTDataclass],
                 items_type: str,
                 locale: Locale,
                 next_page: Optional[str] = None,
                 previous_page: Optional[str] = None):
        self.__keyboard: IInlineKeyboard = InlineKeyboardFactory.create_keyboard()
        self.__items = items
        self.__items_type = items_type
        self.__locale = locale
        self.__next_page = next_page
        self.__previous_page = previous_page

    def get_keyboard(self) -> IInlineKeyboard:
        """
        Создаем клавиатуру

        :return: Готовая клавиатура
        """

        row = []

        for item in self.__items.result:
            button = InlineKeyboardFactory.create_button()
            button.set_text(item.name)
            button.set_callback_data(
                ChoiceFilter(filter_name=item.name, filter_type=self.__items_type).pack()
            )

            row.append(button)

            if len(row) == FiltersChoiceKeyboardCreator.ROW_SIZE:
                self.__keyboard.add_buttons_row(row)

        if len(row):
            self.__keyboard.add_buttons_row(row)

        self.__create_navigation_buttons()

        return self.__keyboard

    def __create_navigation_buttons(self) -> None:
        """
        Создаст кнопки навигации

        :return: None
        """

        row = []

        if self.__previous_page:
            button = InlineKeyboardFactory.create_button()
            button.set_text(i18n().get_text(SystemMessages.BACK_BUTTON_TEXT, self.__locale))
            button.set_callback_data(ShowFilterPage(direction='previous', filter_type=self.__items_type).pack())
            row.append(button)

        if self.__next_page:
            button = InlineKeyboardFactory.create_button()
            button.set_text(i18n().get_text(SystemMessages.FORWARD_BUTTON_TEXT, self.__locale))
            button.set_callback_data(ShowFilterPage(direction='next', filter_type=self.__items_type).pack())
            row.append(button)

        self.__keyboard.add_buttons_row(row)
