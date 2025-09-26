from abstraction.callbacks.CallbackData import CallbackData


class SelectCourse(CallbackData, prefix="select_course"):
    course_name: str


class SelectChapter(CallbackData, prefix="select_chapter"):
    course_name: str
    chapter_number: int


class SelectLesson(CallbackData, prefix="select_lesson"):
    course_name: str
    chapter_number: int
    lesson_number: int
