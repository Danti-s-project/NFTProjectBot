from abc import ABC, abstractmethod


class IUser(ABC):
    """
    Интерфейс-адаптер для объектов User телеграмм-мессенджера
    """

    @abstractmethod
    def get_id(self) -> int:
        """
        Получить идентификатор пользователя

        Returns:
            int: Идентификатор пользователя
        """
        pass

    @abstractmethod
    def get_username(self) -> str | None:
        """
        Получить имя пользователя (username)

        Returns:
            str: Имя пользователя или None, если не установлено
        """
        pass

    @abstractmethod
    def get_full_name(self) -> str:
        """
        Получить полное имя пользователя

        Returns:
            str: Полное имя пользователя
        """
        pass

    @abstractmethod
    def get_language_code(self) -> str | None:
        """
        Получить код языка пользователя

        Returns:
            str | None: Код языка пользователя или None, если не установлен
        """
        pass

    @abstractmethod
    def is_premium(self) -> bool:
        """
        Проверка, имеет ли пользователь премиум-статус

        Returns:
            bool: True, если пользователь имеет премиум-статус, иначе False
        """
        pass
