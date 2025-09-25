from abstraction.callbacks.CallbackData import CallbackData


class SelectCourse(CallbackData, prefix="select_course"):
    course_name: str