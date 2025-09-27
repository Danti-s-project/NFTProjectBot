from typing import Any

from abc import abstractmethod, ABC


class IKeyboard(ABC):
    @abstractmethod
    def get_keyboard_object(self) -> Any:
        """
        Получить объект клавиатуры в формате, необходимом для конкретной реализации

        Returns:
            Any: Объект клавиатуры, готовый для использования в библиотеке
        """
        pass
