import logging

from abstraction.inline_keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from callbacks.profile_callbacks import ProfileAction
from localization_service.LocalesManager import LocalesManager
from localization_service.types import SystemMessages
from localization_service.i18n import i18n
from routers.message_routers.BaseMessageRouter import BaseMessageRouter
from api.APIService import APIService
from api.models import User

logger = logging.getLogger("ProfileRouter")


class ProfileRouter(BaseMessageRouter):

    def __init__(self, message):
        super().__init__(message)

    async def route(self) -> None:
        """
        См. Документацию в абстрактном классе BaseMessageRouter

        :return: None
        """

        user = await APIService().get_user(self._message.get_from_user().get_id())

        # В случае если пользователь еще не вводил команду /start
        if not user:
            logger.debug(f"User {self._message.get_from_user().get_id()} use /profile command, but he doesn't exist")
            await self._message.answer("Pls, send /start command first")
            return

        await self.__send_message(user)

    async def __send_message(self, user: User) -> None:
        """
        Отправить сообщение с профилем

        :param user: Пользователь с нашего API
        :return: None
        """

        locale = await LocalesManager().get_locale(self._message.get_from_user().get_id())

        # Собираем и форматируем текст

        # Полное имя пользователя
        fullname = self._message.get_from_user().get_full_name()

        # Дата регистрации
        registration_date = user.registration_date

        # Язык в боте
        language = "English"
        if user.language == "ru":
            language = "Русский"
        elif user.language == "zh":
            language = "中文"

        # Премиум подписка
        premium_subscribe = i18n().get_text(SystemMessages.PROFILE_SUBSCRIBE_INACTIVE_STATUS, locale)
        if user.is_premium:
            premium_subscribe = i18n().get_text(SystemMessages.PROFILE_SUBSCRIBE_ACTIVE_STATUS, locale)

        # Баланс
        balance = str(user.balance) + " TON"

        # Формируем сообщение
        message = i18n().get_text(SystemMessages.PROFILE_MESSAGE, locale,
                                  fullname,
                                  registration_date,
                                  language,
                                  premium_subscribe,
                                  balance)

        # Формируем клавиатуру
        factory = InlineKeyboardFactory()

        reply_markup = factory.create_keyboard()

        button = factory.create_button()
        button.set_text(i18n().get_text(SystemMessages.SETTINGS_BUTTON_TEXT, locale))
        button.set_callback_data(ProfileAction(action="settings").pack())

        row = reply_markup.add_row()
        row.add_button(button)


        # Отправляем
        await self._message.answer(message, reply_markup=reply_markup)
