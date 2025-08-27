from typing import List

from abstraction.keyboard.IInlineKeyboard import IInlineKeyboard
from abstraction.keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from callbacks.search_callbacks import ShowCollectionsPage, ChoiceCollection


class CollectionChoiceKeyboardCreator:
    """
    Класс создающий клавиатуру для выбора коллекции
    Не является паттерном
    """

    ROW_SIZE = 2

    def __init__(self, collections: List[dict], next_page=None, previous_page=None):
        """
        Конструктор

        :param collections: Список словарей, где каждый словарь это отдельная коллекция
        Выглядит как {"name": ... "alias": ... }
        """

        self.__collections = collections
        self.__next_page = next_page
        self.__previous_page = previous_page
        self.__keyboard = InlineKeyboardFactory.create_keyboard()

    def get_keyboard(self) -> IInlineKeyboard:
        """
        Получить нужную клавиатуру

        :return: Клавиатура
        """

        self.__create_collection_buttons()
        self.__create_navigation_buttons()
        return self.__keyboard

    def __create_collection_buttons(self) -> None:
        """
        Создаст кнопки с названиями коллекций

        :return: None
        """

        row = []

        # Создаем кнопки и добавляем в клавиатуру
        for nft_collection in self.__collections:
            button = InlineKeyboardFactory.create_button()
            button.set_text(nft_collection["alias"])
            button.set_callback_data(ChoiceCollection(collection_name=nft_collection["name"]).pack())

            row.append(button)

            if len(row) == CollectionChoiceKeyboardCreator.ROW_SIZE:
                self.__keyboard.add_buttons_row(row)
                row = []

        if len(row):
            self.__keyboard.add_buttons_row(row)

    def __create_navigation_buttons(self) -> None:
        """
        Создаст кнопки навигации

        :return: None
        """

        row = []

        if self.__previous_page:
            button = InlineKeyboardFactory.create_button()
            button.set_text("Назад")
            button.set_callback_data(ShowCollectionsPage(direction='previous').pack())
            row.append(button)

        if self.__next_page:
            button = InlineKeyboardFactory.create_button()
            button.set_text("Вперед")
            button.set_callback_data(ShowCollectionsPage(direction='next').pack())
            row.append(button)

        self.__keyboard.add_buttons_row(row)