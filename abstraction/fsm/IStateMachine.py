from abc import ABC, abstractmethod
from typing import Optional, Any
from abstraction.fsm.IState import IState


class IStateMachine(ABC):
    """
    Интерфейс для работы с FSM
    """

    @abstractmethod
    async def set_state(self, state: IState) -> None:
        """
        Установить текущее состояние
        """
        pass

    @abstractmethod
    async def get_state(self) -> Optional[str]:
        """
        Получить текущее состояние
        """
        pass

    @abstractmethod
    async def clear_state(self) -> None:
        """
        Очистить текущее состояние
        """
        pass

    @abstractmethod
    async def get_data(self) -> dict[str, Any]:
        """
        Получить data стейта
        :return:
        """

        pass

    @abstractmethod
    async def update_data(self, data: dict[str, Any]) -> None:
        """
        Обновить данные

        :param data: новые данные
        :return: None
        """
