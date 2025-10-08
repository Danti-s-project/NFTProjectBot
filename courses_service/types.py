"""
Типы сервиса courses
"""

import enum
from typing import List

from pydantic import BaseModel


class CoursesEnum(enum.Enum):
    """
    Список курсов
    """

    # TODO: убрать комментарии
    P2P_COURSE = "p2p_course"
    # toncoin_course = "toncoin_course"
    # SCAM_COURSE = "scam_course"
    # NFT_SELL_COURSE = "nft_sell_course"


class LessonPart(BaseModel):
    """
    Часть диалога в уроке

    attrs:
        text: Строка. Текст курса
        answer: Строка. Ответ, который появится в кнопке перехода к следующему уроку
    """

    text: str
    answer: str


class Lesson(BaseModel):
    """
    Урок в главе

    attrs:
        name: Строка. Название урока
        parts: Список частей урока
    """

    name: str
    parts: List[LessonPart]


class Chapter(BaseModel):
    """
    Глава в курсе

    attrs:
        name: Строка. Название главы
        parts: Список уроков в главе
    """

    name: str
    lessons: List[Lesson]


class Course(BaseModel):
    """
    Объект курса

    attrs:
        name: Строка. Название курса
        chapters: Список глав в курсе
        lessons_count: Количество уроков в курсе. Удобное значение для того, чтобы проверить пройден ли курс
    """

    name: str
    alias: str
    chapters: List[Chapter]

    @property
    def lessons_count(self) -> int:
        """
        Получить количество уроков в курсе
        :return: Количество уркоов в курсе
        """

        return sum([len(i.lessons) for i in self.chapters])
