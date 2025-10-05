from routers.fsm_routers.BaseFSMRouter import BaseFSMRouter
from courses_service.CoursesManager import CoursesManager
from courses_service.types import LessonPart, CoursesEnum
from abstraction.reply_keyboard.ReplyKeyboardFactory import ReplyKeyboardFactory
# TODO: Упростить этот упоротый импорт
from localization_service import i18n, SystemMessages, LocalesManager

from api.APIService import APIService


class CourseFSMRouter(BaseFSMRouter):
    async def route(self) -> None:
        await self.__send_new_part()

    async def __send_new_part(self) -> None:
        data = await self._fsm.get_data()

        # Получаем все нужные данные для запроса
        course: str = data.get("course")
        chapter: int = data.get("chapter")
        lesson: int = data.get("lesson")
        part_index: int = data.get("part")
        locale = await LocalesManager().get_locale(self._message.get_from_user().get_id())

        course_manager = CoursesManager()

        lesson_part: LessonPart = course_manager.get_lesson_part(locale, CoursesEnum[course], chapter, lesson, part_index)

        # Если частей больше нет, заканчиваем урок
        if lesson_part is None:
            await self._message.answer(i18n().get_text(SystemMessages.LESSON_IS_OVER, locale), reply_markup=None)
            await APIService().new_completed_lesson(
                self._message.get_from_user().get_id(),
                chapter,
                lesson,
                CoursesEnum[course].value)
            await self._fsm.clear_state()
            return

        # Иначе продолжаем
        keyboard = ReplyKeyboardFactory.create_keyboard()
        keyboard.add_button(ReplyKeyboardFactory.create_button(lesson_part.answer))

        await self._message.answer(lesson_part.text, reply_markup=keyboard)
        await self._fsm.update_data({"part": part_index + 1})
