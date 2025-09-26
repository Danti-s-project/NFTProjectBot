from abstraction.fsm.Aiogram3FSM import Aiogram3FSM
from aiogram.fsm.context import FSMContext


class FSMFactory:
    """
    Фабрика для работы с FSM в aiogram 3.x
    """

    @staticmethod
    def create_fsm(ctx: FSMContext) -> Aiogram3FSM:
        return Aiogram3FSM(ctx)
