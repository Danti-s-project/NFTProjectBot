from typing import List

from routers.message_routers.BaseMessageRouter import BaseMessageRouter
from courses_service.types import CoursesEnum
from courses_service.CoursesManager import CoursesManager
from abstraction.inline_keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from localization_service import i18n, SystemMessages, LocalesManager
from callbacks.courses_callback import SelectCourse


class CourseCommandRouter(BaseMessageRouter):
    async def route(self) -> None:
        await self.__send_message()

    async def __send_message(self) -> None:
        # Создаем клавиатуру

        locale = await LocalesManager().get_locale(self._message.get_from_user().get_id())

        keyboard = InlineKeyboardFactory().create_keyboard()

        completed_courses: List[CoursesEnum] = await CoursesManager().get_completed_courses(self._message.get_from_user().get_id())

        for course in CoursesEnum:
            row = keyboard.add_row()
            button = InlineKeyboardFactory().create_button()
            button.set_callback_data(SelectCourse(course_name=course.name).pack())

            if course in completed_courses:
                icon = "🟢"
            else:
                icon = "🔴"

            button.set_text(icon + " " + CoursesManager().get_course_name(locale, course))
            row.add_button(button)

        text = i18n().get_text(SystemMessages.SELECT_COURSE, locale)

        await self._message.answer(text, reply_markup=keyboard)