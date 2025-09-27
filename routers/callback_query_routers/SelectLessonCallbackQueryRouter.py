from abstraction.reply_keyboard.ReplyKeyboardFactory import ReplyKeyboardFactory
from courses_service.CoursesManager import CoursesManager
from courses_service.types import LessonPart, CoursesEnum
from localization_service.LocalesManager import LocalesManager
from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from fsm.course_fsm.CourseStateGroup import CourseStateGroup
from callbacks.courses_callback import SelectLesson


class SelectLessonCallbackQueryRouter(BaseCallbackQueryRouter):
    async def route(self) -> None:

        data = SelectLesson.unpack(self._callback_query.get_data())

        # Обновляем стейт пользователя
        await self._fsm_state.set_state(CourseStateGroup.lesson)
        await self._fsm_state.set_data({"course": data.course_name, "chapter": data.chapter_number, "lesson": data.lesson_number, "part": 0})

        # Отправляем сообщение
        locale = await LocalesManager().get_locale(self._callback_query.get_from_user().get_id())

        course_manager = CoursesManager()

        lesson_part: LessonPart = course_manager.get_lesson_part(locale, CoursesEnum[data.course_name], data.chapter_number, data.lesson_number, 0)

        # Иначе продолжаем
        keyboard = ReplyKeyboardFactory.create_keyboard()
        keyboard.add_button(ReplyKeyboardFactory.create_button(lesson_part.answer))

        await self._callback_query.get_message().answer(lesson_part.text, reply_markup=keyboard)
