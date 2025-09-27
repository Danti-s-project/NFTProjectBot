from aiogram.fsm.state import State, StatesGroup

from abstraction.fsm.Aiogram3State import Aiogram3State


# TODO: REPLACE AIOGRAM API BY ABSTRACTION!
class CourseStateGroup(StatesGroup):
    """
    Стейт прохождения курсов
    """

    lesson = State()
