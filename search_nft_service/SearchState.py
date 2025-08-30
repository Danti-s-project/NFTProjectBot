from typing import Optional
from api.models import Collection, Backdrop, Symbol, Model

class SearchState:
    """
    Класс хранит в себе параметры поиска NFT конкретного пользователя
    """

    def __init__(self):
        self.next_page: Optional[str] = None
        self.previous_page: Optional[str] = None
        self.collection: Optional[Collection] = None
        self.model: Optional[Model] = None
        self.backdrop: Optional[Backdrop] = None
        self.symbol: Optional[Symbol] = None

