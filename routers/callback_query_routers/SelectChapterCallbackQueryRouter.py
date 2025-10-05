from routers.callback_query_routers.BaseCallbackQueryRouter import BaseCallbackQueryRouter
from abstraction.inline_keyboard.InlineKeyboardFactory import InlineKeyboardFactory
from callbacks.courses_callback import SelectChapter, SelectLesson
from courses_service.CoursesManager import CoursesManager
from courses_service.types import CoursesEnum
from localization_service.LocalesManager import LocalesManager
from localization_service.types import SystemMessages
from localization_service.i18n import i18n


class SelectChapterCallbackQueryRouter(BaseCallbackQueryRouter):
    async def route(self) -> None:
        await self.__send_chapters_message()

    async def __send_chapters_message(self):
        callback_data = SelectChapter.unpack(self._callback_query.get_data())
        locale = await LocalesManager().get_locale(self._callback_query.get_from_user().get_id())

        # Формируем текст
        text = i18n().get_text(SystemMessages.SELECT_LESSON, locale)

        # Формируем клавиатуру

        course_manager = CoursesManager()

        # Получаем прочитанные уроки
        completed_lessons = await course_manager.get_completed_lessons(
            self._callback_query.get_from_user().get_id(),
            CoursesEnum[callback_data.course_name],
            callback_data.chapter_number
        )

        # Получаем список уроков в главе
        lesson_names = course_manager.get_chapter_lesson_names(locale, CoursesEnum[callback_data.course_name],
                                                               callback_data.chapter_number)

        # Создаем объект клавиатуры
        keyboard_factory = InlineKeyboardFactory()

        keyboard = keyboard_factory.create_keyboard()

        # TODO: Оптимизируй перебор

        for lesson in range(len(lesson_names)):
            if lesson in completed_lessons:
                icon = "🟢"
            else:
                icon = "🔴"

            text = icon + lesson_names[lesson]

            row = keyboard.add_row()
            button_callback_data: str = SelectLesson(
                chapter_number=callback_data.chapter_number,
                course_name=callback_data.course_name,
                lesson_number=lesson).pack()
            button = keyboard_factory.create_button()
            button.set_text(text).set_callback_data(button_callback_data)
            row.add_button(button)

        # Когда все готово, отправляем сообщение

        # TODO: Превратить все в один запрос
        await self._callback_query.get_message().edit_message(text=text, reply_markup=keyboard)
