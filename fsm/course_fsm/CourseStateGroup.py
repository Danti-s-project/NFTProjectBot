from aiogram.fsm.state import State, StatesGroup


class CourseStateGroup(StatesGroup):
    """
    Стейт прохождения курсов
    """

    lesson = State()
