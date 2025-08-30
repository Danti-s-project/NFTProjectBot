"""
Здесь расписаны все модели из API
Модели нужны для введения объектной природы для каждого response
"""
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, List


T = TypeVar('T')


# Модели объектов NFT

@dataclass
class BaseNFTDataclass:
    name: str


@dataclass
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


@dataclass
class Owner(BaseNFTDataclass):
    pass


@dataclass
class Model(BaseNFTDataclass):
    pass


@dataclass
class Backdrop(BaseNFTDataclass):
    pass


@dataclass
class Symbol(BaseNFTDataclass):
    pass


@dataclass
class NFT:
    collection: Collection
    owner: Owner
    model: Model
    backdrop: Backdrop
    symbol: Symbol


# Модели сервиса Users

@dataclass
class User:
    user_id: int
    username: str
    fullname: str
    registration_date: str
    language: str
    ref_user: Optional[int]
    is_premium: bool
    balance: float


# Модели ответов

@dataclass
class PaginationAPIReponse(Generic[T]):
    count: int
    next: Optional[str]
    previous: Optional[str]
    result: List[T]


@dataclass
class NFTSAPIResponse:
    result: List[NFT]
    

