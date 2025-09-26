from aiogram.fsm.context import FSMContext
from abstraction.fsm.IStateMachine import IStateMachine
from abstraction.fsm.IState import IState


class Aiogram3FSM(IStateMachine):
    """
    Адаптер для FSMContext aiogram 3.x
    """

    def __init__(self, fsm_context: FSMContext):
        self._ctx = fsm_context

    async def set_state(self, state: IState) -> None:
        await self._ctx.set_state(state.get_name())

    async def get_state(self) -> str | None:
        return await self._ctx.get_state()

    async def clear_state(self) -> None:
        await self._ctx.clear()
