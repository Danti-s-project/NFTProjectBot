from abc import ABC, abstractmethod
from typing import List
from abstraction.fsm.IState import IState


class IStateGroup(ABC):
    """
    Интерфейс для группы состояний
    """

    @abstractmethod
    def get_states(self) -> List[IState]:
        """
        Получить список состояний группы
        """
        pass
