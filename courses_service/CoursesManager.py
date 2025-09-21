from typing import List, Dict
import json

from courses_service.types import CoursesEnum, Course, LessonPart, Lesson, Chapter

# TODO: logging + end this


class CoursesManager:
    """
    Менеджер
    """


    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(CoursesManager, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance


    def __init__(self, *args, **kwargs):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True
            self.__init(*args, **kwargs)


    def __init(self, *args, **kwargs):
        # Загрузка локалей в оперативку

        pass

    def __load_courses(self, file_name: str) -> Dict[CoursesEnum, Course]:
        result = {}

        with open(file_name, 'r', encoding='utf-8') as f:
            courses = json.load(f)

        for course in courses:
            course_object = self.__serialize_course(course)

            match course_object.name:
                case "p2p_course":
                    result[CoursesEnum.P2P_COURSE] = course_object
                case "toncoin_course":
                    result[CoursesEnum.TONCOIN_COURSE] = course_object
                case "scam_course":
                    result[CoursesEnum.SCAM_COURSE] = course_object
                case "nft_sell_course":
                    result[CoursesEnum.NFT_SELL_COURSE] = course_object
                case _:
                    raise ValueError(f"Unknown course {course_object}! Please check {file_name}")

        return result

    def __serialize_course(self, course: dict) -> Course:
        """
        Сериализовать курс из json в объектную природу

        :param course: Загруженный курс из json
        :return: Курс
        """

        course_object = Course(name=course["name"], alias=course["alias"], chapters=[], lessons_count=0)

        for chapter in course["chapters"]:
            chapter_object = self.__serialize_chapter(chapter)
            course_object.chapters.append(chapter_object)
            course_object.lessons_count += len(chapter_object.lessons)

        return course_object

    def __serialize_chapter(self, chapter: dict) -> Chapter:
        """
        Сериализовать главу из json в объектую природу

        :param chapter: Загруженная глава из json
        :return: Объект главы
        """

        chapter_object = Chapter(name=chapter["name"], lessons=[])

        for lesson in chapter["lessons"]:
            chapter_object.lessons.append(self.__serialize_lesson(lesson))

        return chapter_object

    def __serialize_lesson(self, lesson: dict) -> Lesson:
        """
        Сериализовать урок из json в объектую природу

        :param lesson: Загруженный урок из json
        :return: Объект урока
        """

        lesson_object = Lesson(name=lesson["name"], parts=[])

        for part in lesson["parts"]:
            lesson_object.parts.append(self.__serialize_lesson_part(part))

        return lesson_object

    def __serialize_lesson_part(self, lesson_part: dict) -> LessonPart:
        """
        Сериализовать часть урока из json в объектую природу
/
        :param lesson_part: Загруженная часть урока из json
        :return: Объект части урока
        """

        lesson_part = LessonPart(text=lesson_part["text"], answer=lesson_part["answer"])

        return lesson_part


    async def get_completed_courses(self, user_id: int) -> List[CoursesEnum]:
        pass

    async def get_completed_chapters(self, user_id: int, course: CoursesEnum) -> List[int]:
        pass

    async def get_completed_lessons(self, user_id: int, course: CoursesEnum, chapter: int) -> List[int]:
        pass
