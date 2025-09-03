from aiogram.types import User

from abstraction.IUser import IUser


class Aiogram3User(IUser):
    """
    Адаптер для объекта User из библиотеки aiogram версии 3.x
    """

    def __init__(self, user: User):
        """
        Инициализация адаптера для пользователя

        Args:
            user (User): Объект пользователя aiogram
        """
        self._user = user

    def get_id(self) -> int:
        """
        Получить идентификатор пользователя

        Returns:
            int: Идентификатор пользователя
        """
        return self._user.id

    def get_username(self) -> str | None:
        """
        Получить имя пользователя (username)

        Returns:
            str: Имя пользователя или None, если не установлено
        """
        return self._user.username

    def get_full_name(self) -> str:
        """
        Получить полное имя пользователя

        Returns:
            str: Полное имя пользователя
        """
        return self._user.full_name

    def get_language_code(self) -> str | None:
        """
        Получить код языка пользователя

        Returns:
            str | None: Код языка пользователя или None, если не установлен
        """
        return self._user.language_code

    def is_premium(self) -> bool:
        """
        Проверка, имеет ли пользователь премиум-статус

        Returns:
            bool: True, если пользователь имеет премиум-статус, иначе False
        """
        return self._user.is_premium
