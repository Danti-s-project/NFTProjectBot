from abc import ABC, abstractmethod


class IState(ABC):
    """
    Интерфейс для отдельного состояния
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        Получить имя состояния
        """
        pass
