"""
Типы сервиса courses
"""

import enum
from typing import List
from dataclasses import dataclass


class CoursesEnum(enum.Enum):
    """
    Список курсов
    """

    P2P_COURSE = "p2p_course"
    # toncoin_course = "toncoin_course"
    # SCAM_COURSE = "scam_course"
    # NFT_SELL_COURSE = "nft_sell_course"


@dataclass
class LessonPart:
    """
    Часть диалога в уроке

    attrs:
        text: Строка. Текст курса
        answer: Строка. Ответ, который появится в кнопке перехода к следующему уроку
    """

    text: str
    answer: str


@dataclass
class Lesson:
    """
    Урок в главе

    attrs:
        name: Строка. Название урока
        parts: Список частей урока
    """

    name: str
    parts: List[LessonPart]


@dataclass
class Chapter:
    """
    Глава в курсе

    attrs:
        name: Строка. Название главы
        parts: Список уроков в главе
    """

    name: str
    lessons: List[Lesson]


@dataclass
class Course:
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
    lessons_count: int
