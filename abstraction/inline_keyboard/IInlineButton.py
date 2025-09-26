from abc import ABC, abstractmethod
from typing import Any, Optional


class IInlineButton(ABC):
    """
    Интерфейс для инлайн-кнопок в мессенджере
    """

    @abstractmethod
    def set_text(self, text: str) -> 'IInlineButton':
        """
        Установить текст кнопки

        Args:
            text: Текст, отображаемый на кнопке

        Returns:
            IInlineButton: Текущий объект кнопки для цепочки вызовов
        """
        pass

    @abstractmethod
    def set_callback_data(self, callback_data: str) -> 'IInlineButton':
        """
        Установить данные обратного вызова для кнопки

        Args:
            callback_data: Строка с данными, которые будут отправлены при нажатии на кнопку

        Returns:
            IInlineButton: Текущий объект кнопки для цепочки вызовов
        """
        pass

    @abstractmethod
    def set_url(self, url: str) -> 'IInlineButton':
        """
        Установить URL для кнопки

        Args:
            url: Ссылка, на которую будет перенаправлен пользователь при нажатии

        Returns:
            IInlineButton: Текущий объект кнопки для цепочки вызовов
        """
        pass

    @abstractmethod
    def get_button_object(self) -> Any:
        """
        Получить объект кнопки в формате, необходимом для конкретной реализации

        Returns:
            Any: Объект кнопки, готовый для использования в библиотеке
        """
        pass
