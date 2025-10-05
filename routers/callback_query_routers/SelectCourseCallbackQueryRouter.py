from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from abstraction.inline_keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from callbacks.courses_callback import SelectCourse, SelectChapter
from courses_service.CoursesManager import CoursesManager
from courses_service.types import CoursesEnum
from localization_service.LocalesManager import LocalesManager
from localization_service.types import SystemMessages
from localization_service.i18n import i18n


class SelectCourseCallbackQueryRouter(BaseCallbackQueryRouter):
    async def route(self) -> None:
        await self.__send_chapters_message()

    async def __send_chapters_message(self):
        callback_data = SelectCourse.unpack(self._callback_query.get_data())
        locale = await LocalesManager().get_locale(self._callback_query.get_from_user().get_id())

        # Формируем текст
        text = i18n().get_text(SystemMessages.SELECT_CHAPTER, locale)

        # Формируем клавиатуру

        course_manager = CoursesManager()

        # Получаем прочитанные главы
        completed_chapters = await course_manager.get_completed_chapters(
            self._callback_query.get_from_user().get_id(),
            CoursesEnum[callback_data.course_name]
        )

        # Получаем список всех глав в курсе
        chapter_names = course_manager.get_course_chapter_names(locale, CoursesEnum[callback_data.course_name])

        # Создаем объект клавиатуры
        keyboard_factory = InlineKeyboardFactory()

        keyboard = keyboard_factory.create_keyboard()

        for chapter in range(len(chapter_names)):
            if chapter in completed_chapters:
                icon = "🟢"
            else:
                icon = "🔴"

            text = icon + chapter_names[chapter]

            row = keyboard.add_row()
            button_callback_data: str = SelectChapter(chapter_number=chapter, course_name=callback_data.course_name).pack()
            button = keyboard_factory.create_button()
            button.set_text(text).set_callback_data(button_callback_data)
            row.add_button(button)


        # Когда все готово, отправляем сообщение

        await self._callback_query.get_message().edit_message(text=text, reply_markup=keyboard)
