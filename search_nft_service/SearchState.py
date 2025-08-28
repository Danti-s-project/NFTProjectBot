from typing import Optional

class SearchState:
    """
    Класс хранит в себе параметры поиска NFT конкретного пользователя
    """

    def __init__(self):
        self.next_page: Optional[str] = None
        self.previous_page: Optional[str] = None
        self.collection_name: Optional[str] = None
        self.model: Optional[str] = None
        self.backdrop: Optional[str] = None
        self.symbol: Optional[str] = None

