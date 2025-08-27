class SearchState:
    """
    Класс хранит в себе параметры поиска NFT конкретного пользователя
    """

    def __init__(self):
        self.next_page = None
        self.previous_page = None
        self.collection_name = None
        self.model = None
        self.backdrop = None
        self.symbol = None

