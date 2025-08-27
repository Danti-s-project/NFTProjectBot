from aiogram.types import CallbackQuery

from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from abstraction.keyboard.IInlineKeyboard import IInlineKeyboard
from abstraction.keyboard.IInlineButton import IInlineButton
from abstraction.keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from search_nft_service.SearchStateManager import SearchStateManager
from callbacks.search_callbacks import ChoiceCollection, Action


class ChoiceCollectionCallbackQueryRouter(BaseCallbackQueryRouter):

    def __init__(self, callback_query: CallbackQuery):
        super().__init__(callback_query)

    async def route(self) -> None:
        self.__write_collection_name()
        await self.__send_filters_message()

    def __write_collection_name(self) -> None:
        """
        Записываем название коллекции, которую ищет пользователь, в его статус

        :return: None
        """

        data = ChoiceCollection.unpack(self.__callback_query.get_data())
        SearchStateManager().get(
            self.__callback_query.get_from_user().get_id()
        ).collection_name = data.collection_name

    async def __send_filters_message(self) -> None:
        """
        Отправить сообщение с клавиатурой в чат

        :return: None
        """
        keyboard = self.__create_keyboard()
        await self.__callback_query.get_message().answer(
            "Выставите фильтры:", reply_markup=keyboard)

    def __create_keyboard(self) -> IInlineKeyboard:
        """
        Создание inline клавиатуры

        :return: имплементация IInlineKeyboard
        """

        inline_keyboard = InlineKeyboardFactory.create_keyboard()

        model_button: IInlineButton = InlineKeyboardFactory.create_button()
        model_button.set_text("Выбрать модель")
        model_button.set_callback_data(Action(action="model").pack())

        backdrop_button: IInlineButton = InlineKeyboardFactory.create_button()
        backdrop_button.set_text("Выбрать фон")
        backdrop_button.set_callback_data(Action(action="backdrop").pack())

        symbol_button: IInlineButton = InlineKeyboardFactory.create_button()
        symbol_button.set_text("Выбрать символ")
        symbol_button.set_callback_data(Action(action="symbol").pack())

        search_button: IInlineButton = InlineKeyboardFactory.create_button()
        search_button.set_text("Поиск")
        search_button.set_callback_data(Action(action="search").pack())

        inline_keyboard.add_buttons_row([model_button, backdrop_button, symbol_button])
        inline_keyboard.add_buttons_row([search_button])

        return inline_keyboard
