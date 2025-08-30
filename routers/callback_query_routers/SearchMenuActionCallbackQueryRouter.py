import os

from abstraction.keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from abstraction.IMessage import IMessageAdapter
from api.APIService import APIService
from api.models import NFTSAPIResponse, BaseDataclass, PaginationAPIReponse, Symbol, Model, Backdrop
from search_nft_service.keyboard_creators.FiltersChoiceKeyboardCreate import FiltersChoiceKeyboardCreator
from search_nft_service.SearchStateManager import SearchStateManager
from callbacks.search_callbacks import Action, Back


class SearchMenuActionCallbackQueryRouter(BaseCallbackQueryRouter):
    """
    Роутер обрабатывающий все нажатия в главном меню /search
    """

    HOST = os.getenv("HOST")
    PAGE_LIMIT = 2

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

        result: NFTSAPIResponse = await APIService().get_nfts(
            search_state.collection,
            model=search_state.model,
            backdrop=search_state.backdrop,
            symbol=search_state.symbol
        )

        message = f"Найдено {len(result.result)} NFT по запросу: \n\n Коллекция: {search_state.collection.name}\n"
        if search_state.model:
            message += f"Модель: {search_state.model}\n"
        if search_state.backdrop:
            message += f"Фон: {search_state.backdrop}\n"
        if search_state.symbol:
            message += f"Символ: {search_state.symbol}\n"

        message += "\n\n"

        for item in result.result:
            message += \
                (f"{item.collection.name}:\n"
                 f"Модель:{item.model.name}\n"
                 f"Символ: {item.symbol.name}\n"
                 f"Фон: {item.backdrop.name}\n")

            if item.owner:
                message += f"Владелец: {item.owner.name}"

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
        data: PaginationAPIReponse[Model] = await APIService().get_models(
            f"{SearchMenuActionCallbackQueryRouter.HOST}"
            f"/api/v1/nfts/models/?offset=0&limit={SearchMenuActionCallbackQueryRouter.PAGE_LIMIT}")
        search_state.next_page = data.next

        keyboard = FiltersChoiceKeyboardCreator(data, data.next).get_keyboard()

        message: IMessageAdapter = self.__callback_query.get_message()
        await message.edit_reply_markup(reply_markup=keyboard)
        await message.edit_message_text("Выберите модель:")

    async def __backdrop_menu_action(self) -> None:
        """
        Выполняет действия после нажатия кнопки фон

        :return: None
        """

        search_state = SearchStateManager().get(self.__callback_query.get_from_user().get_id())
        data: PaginationAPIReponse[Backdrop] = await APIService().get_backdrops(
            f"{SearchMenuActionCallbackQueryRouter.HOST}"
            f"/api/v1/nfts/backdropss/?offset=0&limit={SearchMenuActionCallbackQueryRouter.PAGE_LIMIT}")
        search_state.next_page = data.next

        keyboard = FiltersChoiceKeyboardCreator(data, data.next).get_keyboard()

        message: IMessageAdapter = self.__callback_query.get_message()
        await message.edit_reply_markup(reply_markup=keyboard)
        await message.edit_message_text("Выберите фон:")

    async def __symbol_menu_action(self) -> None:
        """
        Выполняет действия после нажатия кнопки символ

        :return: None
        """

        search_state = SearchStateManager().get(self.__callback_query.get_from_user().get_id())
        data: PaginationAPIReponse[Symbol] = await APIService().get_symbols(
            f"{SearchMenuActionCallbackQueryRouter.HOST}"
            f"/api/v1/nfts/symbols/?offset=0&limit={SearchMenuActionCallbackQueryRouter.PAGE_LIMIT}")

        search_state.next_page = data.next

        keyboard = FiltersChoiceKeyboardCreator(data, data.next).get_keyboard()

        message: IMessageAdapter = self.__callback_query.get_message()
        await message.edit_reply_markup(reply_markup=keyboard)
        await message.edit_message_text("Выберите символ:")
