from aiogram.fsm.state import StatesGroup
from abstraction.fsm.IStateGroup import IStateGroup
from abstraction.fsm.IState import IState
from abstraction.fsm.Aiogram3State import Aiogram3State


class Aiogram3StateGroup(IStateGroup, StatesGroup):
    """
    Адаптер для группы состояний aiogram 3.x
    """

    def get_states(self) -> list[IState]:
        return [Aiogram3State(state) for state in self.__all_states__]
