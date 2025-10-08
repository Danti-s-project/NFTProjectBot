from typing import List, Dict, Optional, Set
import logging
import json

from api.APIService import APIService
from api.models import CoursesAPIResponse
from courses_service.types import CoursesEnum, Course, LessonPart, Lesson, Chapter
from localization_service import Locale


logger = logging.getLogger('CoursesManager')


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
        self.__ru_course = self.__load_courses("courses_ru.json")
        self.__en_course = self.__load_courses("courses_en.json")
        self.__zh_course = self.__load_courses("courses_zh.json")

        logger.info("Courses manager успешно инициализирован!")

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
                    logger.critical(f"Unknown course {course_object}! Please check {file_name}")
                    raise ValueError(f"Unknown course {course_object}! Please check {file_name}")

        logger.info(f"{file_name} course was successfully loaded!")

        return result

    def __serialize_course(self, course: dict) -> Course:
        """
        Сериализовать курс из json в объектную природу

        :param course: Загруженный курс из json
        :return: Курс
        """

        return Course(**course)

    async def get_completed_courses(self, user_id: int) -> List[CoursesEnum]:
        """
        Получить список завершенных курсов

        :param user_id: айди пользователя
        :return: Список завершенных курсов
        """

        api_service = APIService()
        result = []

        for course in CoursesEnum:
            response: List[CoursesAPIResponse] = await api_service.get_completed_lessons(course.value, user_id)
            if len(response) == self.__en_course[course].lessons_count:
                result.append(course)

        return result

    async def get_completed_chapters(self, user_id: int, course_enum: CoursesEnum) -> Set[int]:
        """
        Получить завершенные главы

        :param user_id: Айди пользователя
        :param course_enum: Курс по которому нужно вернуть завершенные главы
        :return: Список номеров глав
        """

        api_service = APIService()
        result = set()

        response: List[CoursesAPIResponse] = await api_service.get_completed_lessons(course_enum.value, user_id)

        # Перебираем каждую главу в курсе
        for chapter in range(len(self.__ru_course[course_enum].chapters)):
            lessons = 0

            # Перебираем все пройденные уроки пользователем
            for i in response:
                # Если пройденный урок из главы, добавляем к пройденным урокам
                if i.chapter == chapter:
                    lessons += 1

            # Если количество пройденных уроков равно количеству уроков в главе, добавляем в массив
            if len(self.__en_course[course_enum].chapters[chapter].lessons) == lessons:
                result.add(chapter)

        return result

    async def get_completed_lessons(self, user_id: int, course_enum: CoursesEnum, chapter: int) -> Set[int]:
        """
        Получить завершенные уроки

        :param user_id: Айди пользователя
        :param course_enum: Курс по которому нужно что-либо найти
        :param chapter: Номер главы
        :return: None
        """

        api_service = APIService()
        result = set()

        response: List[CoursesAPIResponse] = await api_service.get_completed_lessons(course_enum.value, user_id)

        for course in response:
            if course.chapter == chapter:
                result.add(course.lesson)

        return result

    def __get_locale_dict(self, locale: Locale) -> Dict[CoursesEnum, Course]:
        """
        Получить json с информацией о курсах, в зависимости от языка пользователя

        :param locale: язык пользователя
        :return: json с информацией о курсах
        """

        match locale:
            case Locale.EN:
                return self.__en_course
            case Locale.RU:
                return self.__ru_course
            case Locale.ZH:
                return self.__zh_course
            case _:
                logger.critical("ATTEMPT TO GET UNKNOWN LOCALE!")
                return {}

    def get_course_name(self, locale: Locale, course: CoursesEnum) -> str:
        """
        Получить название курса на нужной локали

        :param locale: язык интерфейса
        :param course: объект курса
        :return: Название курса
        """

        locale_courses = self.__get_locale_dict(locale)
        return locale_courses[course].alias

    def get_course_chapter_names(self, locale: Locale, course: CoursesEnum) -> List[str]:
        """
        Получить названия всех глав в курсе

        :param locale: язык курса (Locale курс)
        :param course: объект курса
        :return: Список имен глав
        """

        locale_courses = self.__get_locale_dict(locale)
        course = locale_courses[course]
        return [i.name for i in course.chapters]

    def get_chapter_lesson_names(self, locale: Locale, course: CoursesEnum, chapter_index: int) -> List[str]:
        """
        Получить названия всех уроков в главе

        :param locale: язык курса (Locale курс)
        :param course: объект курса
        :param chapter_index: индекс главы
        :return: Список имен глав
        """

        locale_courses = self.__get_locale_dict(locale)
        course = locale_courses[course]
        chapter = course.chapters[chapter_index]
        return [i.name for i in chapter.lessons]

    def get_lesson_part(
            self,
            locale: Locale,
            course: CoursesEnum,
            chapter_index: int,
            lesson_index: int,
            part_index: int) -> Optional[LessonPart]:

        """
        Получить lesson part по индексам, или None, если LessonPart не существует в курсе

        :param locale: язык интерфейса
        :param course: курс
        :param chapter_index: номер главы
        :param lesson_index: номер урока
        :param part_index: номер части
        :return:
        """

        locale_courses = self.__get_locale_dict(locale)
        course = locale_courses[course]
        chapter = course.chapters[chapter_index]
        lesson = chapter.lessons[lesson_index]

        # Если следующего урока не существует
        if part_index >= len(lesson.parts):
            return None

        return lesson.parts[part_index]
