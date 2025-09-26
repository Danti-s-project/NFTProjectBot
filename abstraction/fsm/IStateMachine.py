from abc import ABC, abstractmethod
from typing import Optional
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
