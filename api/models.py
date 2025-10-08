"""
Здесь расписаны все модели из API
Модели нужны для введения объектной природы для каждого response
"""
from typing import TypeVar, Generic, Optional, List

from pydantic import BaseModel

T = TypeVar('T')


# Модели объектов NFT

class BaseNFTDataclass(BaseModel):
    name: str


class Collection(BaseNFTDataclass):
    indexed: Optional[int]
    quantity: Optional[int]

    @property
    def alias(self):
        """
        Изначально поле alias задумывалось как поле, хранящее имя коллекции в красивом виде
        Так как alias это name без знаков "-", было решено убрать его из полей
        И оставить только property заменяющим знаки - на пробелы

        :return: Косметическое название коллекции
        """
        return self.name.replace("-", " ")


class Owner(BaseNFTDataclass):
    pass


class Model(BaseNFTDataclass):
    pass


class Backdrop(BaseNFTDataclass):
    pass


class Symbol(BaseNFTDataclass):
    pass


class NFT(BaseModel):
    collection: Collection
    owner: Owner
    model: Model
    backdrop: Backdrop
    symbol: Symbol


# Модели сервиса Users

class User(BaseModel):
    user_id: int
    username: str
    fullname: str
    registration_date: str
    language: str
    ref_user: Optional[int]
    is_premium: bool
    balance: float


# Модели ответов

class PaginationAPIResponse(BaseModel, Generic[T]):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[T]


class NFTSAPIResponse(BaseModel):
    result: List[NFT]


class CoursesAPIResponse(BaseModel):
    user_id: int
    chapter: int
    lesson: int
