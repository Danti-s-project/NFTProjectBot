import os

import aiohttp
from aiohttp import ClientSession

from abstraction.keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from abstraction.IMessage import IMessageAdapter
from search_nft_service.keyboard_creators.FiltersChoiceKeyboardCreate import FiltersChoiceKeyboardCreator
from search_nft_service.SearchStateManager import SearchStateManager
from callbacks.search_callbacks import Action, Back


class SearchMenuActionCallbackQueryRouter(BaseCallbackQueryRouter):
    """
    Роутер обрабатывающий все нажатия в главном меню /search
    """

    async def route(self) -> None:
        data = Action.unpack(self.__callback_query.get_data())

        match data.action:
            case "search":
                await self.__search_menu_action()
            case "model":
                await self.__model_menu_action()
            case "backdrop":
                await self.__backdrop_menu_action()
            case "symbol":
                await self.__symbol_menu_action()

    async def __search_menu_action(self) -> None:
        """
        Выполняет действия после нажатия кнопки поиск

        :return: None
        """

        search_state = SearchStateManager().get(self.__callback_query.get_from_user().get_id())

        # Формируем параметры запроса
        params = f"?collection={search_state.collection_name}"
        if search_state.model:
            params += f"&model={search_state.model}"
        if search_state.backdrop:
            params += f"&backdrop={search_state.backdrop}"
        if search_state.symbol:
            params += f"&symbol={search_state.symbol}"

        result = []

        async with ClientSession() as session:
            async with session.get(
                    f"{os.getenv('HOST')}/api/v1/nfts/nfts/{params}") as response:
                data = await response.json()
                result = data["result"]

        message = f"Найдено {len(result)} NFT по запросу: \n\n Коллекция: {search_state.collection_name}\n"
        if search_state.model:
            message += f"Модель: {search_state.model}\n"
        if search_state.backdrop:
            message += f"Фон: {search_state.backdrop}\n"
        if search_state.symbol:
            message += f"Символ: {search_state.symbol}\n"

        message += "\n\n"

        for item in result:
            message += \
                (f"{item['name']} #{item['issued']}:\n"
                 f"Модель:{item['model']}\n"
                 f"Символ: {item['symbol']}"
                 f"Фон: {item['backdrop']}\n")

            if item["owner"]:
                message += f"Владелец: {item['owner']}"

            message += "\n\n"


        # Создаем клавиатуру для сообщения

        keyboard = InlineKeyboardFactory.create_keyboard()

        back_button = InlineKeyboardFactory.create_button()
        back_button.set_text("Назад")
        back_button.set_callback_data(Back().pack())
        keyboard.add_buttons_row([back_button])

        await self.__callback_query.get_message().edit_message_text(message)
        await self.__callback_query.get_message().edit_reply_markup(reply_markup=keyboard)

    async def __model_menu_action(self) -> None:
        """
        Выполняет действия после нажатия кнопки модель

        :return: None
        """

        search_state = SearchStateManager().get(self.__callback_query.get_from_user().get_id())
        data = await self.__request_items("models")

        search_state.next_page = data["next"]

        keyboard = FiltersChoiceKeyboardCreator(data["result"], data["next"]).get_keyboard()

        message: IMessageAdapter = self.__callback_query.get_message()
        await message.edit_reply_markup(reply_markup=keyboard)
        await message.edit_message_text("Выберите модель:")

    async def __backdrop_menu_action(self) -> None:
        """
        Выполняет действия после нажатия кнопки фон

        :return: None
        """

        search_state = SearchStateManager().get(self.__callback_query.get_from_user().get_id())
        data = await self.__request_items("backdrops")

        search_state.next_page = data["next"]

        keyboard = FiltersChoiceKeyboardCreator(data["result"], data["next"]).get_keyboard()

        message: IMessageAdapter = self.__callback_query.get_message()
        await message.edit_reply_markup(reply_markup=keyboard)
        await message.edit_message_text("Выберите фон:")

    async def __symbol_menu_action(self) -> None:
        """
        Выполняет действия после нажатия кнопки символ

        :return: None
        """

        search_state = SearchStateManager().get(self.__callback_query.get_from_user().get_id())
        data = await self.__request_items("symbols")

        search_state.next_page = data["next"]

        keyboard = FiltersChoiceKeyboardCreator(data["result"], data["next"]).get_keyboard()

        message: IMessageAdapter = self.__callback_query.get_message()
        await message.edit_reply_markup(reply_markup=keyboard)
        await message.edit_message_text("Выберите символ:")

    async def __request_items(self, items_name: str) -> dict:
        """
        Так как представление объектов backdrop, model, symbol одинаково {"name": "name"}
        Запрос к серверу можно выделить в отдельный метод

        :param items_name: название объекта для поиска
        :return: результат запроса
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{os.getenv("HOST")}/api/v1/nfts/{items_name}/") as response:
                return await response.json()
