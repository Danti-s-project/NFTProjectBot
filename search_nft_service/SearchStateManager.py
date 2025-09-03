from typing import Optional
from collections import OrderedDict
import logging

from search_nft_service.SearchState import SearchState

class SearchStateManager:
    """
    Объект-менеджер руководящий всеми SearchState
    Singleton
    """

    _instance = None
    logger = logging.getLogger('SearchStateManager')

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(SearchStateManager, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True
            self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        self.__capacity: int = 32676
        self.__search_states: OrderedDict[int, SearchState] = OrderedDict()
        self.logger.info(f"Инициализирован SearchStateManager с емкостью {self.__capacity}")

    # С __search_states запрещено работать напрямую
    # Для взаимодействия со стейтами при помощи методов ниже

    def get(self, user_id: int) -> Optional[SearchState]:
        """
        Получить SearchState по user_id

        :param user_id: айди пользователя
        :return: SearchState
        """
        if user_id not in self.__search_states:
            self.logger.debug(f"SearchState не найден для пользователя {user_id}")
            return None

        self.logger.debug(f"Получен SearchState для пользователя {user_id}")
        self.__search_states.move_to_end(user_id)
        return self.__search_states[user_id]

    def create(self, user_id: int) -> None:
        """
        Создать новый SearchState в менеджере

        :param user_id: user_id пользователя
        :return: None
        """

        self.__search_states[user_id] = SearchState()
        self.__search_states.move_to_end(user_id)
        self.logger.info(f"Создан новый SearchState для пользователя {user_id}")

        if len(self.__search_states) > self.__capacity:
            removed_user_id, _ = self.__search_states.popitem(last=False)
            self.logger.warning(f"Превышена емкость кэша. Удален SearchState пользователя {removed_user_id}")

    def remove(self, user_id: int) -> None:
        """
        Удалить SearchState

        :param user_id: telegram user_id
        :return: None
        """
        if self.__search_states.get(user_id) is not None:
            del self.__search_states[user_id]
            self.logger.info(f"Удален SearchState пользователя {user_id}")
        else:
            self.logger.debug(f"Попытка удаления несуществующего SearchState для пользователя {user_id}")
