from aiogram.fsm.state import State
from abstraction.fsm.IState import IState


class Aiogram3State(IState):
    """
    Адаптер для состояния aiogram 3.x
    """

    def __init__(self, state: State):
        self._state = state

    def get_name(self) -> str:
        return self._state.state
