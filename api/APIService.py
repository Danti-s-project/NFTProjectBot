"""
Здесь описана вся работа с aiohttp
Убедительно рекомендую не использовать import aiohttp вне этого модуля/класса
Это нужно для безопасности

Если вам нужно отправить запрос, которого еще нет в APIService, то просто внесите его
"""


import os
import logging
from typing import TypeVar, Type, Optional

import aiohttp
import dotenv
from aiohttp import ClientSession

from api.models import (PaginationAPIReponse,
                        Collection,
                        Model,
                        Backdrop,
                        Symbol,
                        Owner,
                        NFT,
                        NFTSAPIResponse,
                        User)
from api.types import REQUEST_TYPE

dotenv.load_dotenv()

logger = logging.getLogger('APIService')


T = TypeVar('T')

# TODO: Сделать так, чтобы хранилась не ссылка на пагинацию а оффсеты и лимиты

class APIService:
    """
    Сервис для работы с API
    Singleton паттерн
    """

    HOST = os.getenv('HOST')

    _instance = None


    class Response:
        """
        Адаптер для aiohttp.ClientSession
        Нужен для хранения информации о запросе после закрытия aiohttp.ClientSession
        Должен повторять интерфейс aiohttp.ClientResponse. Реализуйте методы по мере надобности
        """

        def __init__(self, status: int, json: dict):
            self.__status = status
            self.__json = json

        @property
        def status(self) -> int:
            """
            Статус ответа

            :return: Статус (INT)
            """

            return self.__status

        async def json(self) -> dict:
            """
            метод json в aiohttp.ClientResponse - асинхронныый.
            Сделаю его асинхронным и здесь, чтобы не нарушать совместимости

            :return: тело ответа
            """

            return self.__json

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(APIService, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance

    def __init__(self):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set an initial flag to True
            self.__init()

    def __init(self):
        """
        Singleton паттерн требует писать функционал конструктора здесь.

        :return: None
        """
        self.__session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        """
        Получить старый или создать новый объект ClientSession

        :return: aiohttp.ClientSession
        """

        # TODO: Пошамань с параметрами

        if self.__session is None or self.__session.closed:
            self.__session = aiohttp.ClientSession(
                base_url=APIService.HOST,
                connector=aiohttp.TCPConnector(
                    limit=100,
                    keepalive_timeout=30,
                    force_close=False,
                    enable_cleanup_closed=True
                ),
                timeout=aiohttp.ClientTimeout(
                    total=60,
                    connect=30,
                    sock_connect=30,
                    sock_read=30
                ),
                headers={
                    'Accept': 'application/json',
                    'Connection': 'keep-alive'
                }
            )

        return self.__session

    async def __make_request(
            self,
            request_type: REQUEST_TYPE,
            url: str,
            json=None,
            **kwargs
    ) -> Optional[Response]:

        """
        Общий метод для отправки запросов к API
        Настоятельно рекомендуется использовать именно его для запросов

        :param request_type: types.REQUEST_TYPE - метод запроса (get, post, put)
        :param url: URL для запроса
        :param json: JSON в запросе к серверу
        :param kwargs: Другие аргументы, которые возможно передать в запрос

        :return: aiohttp.ClientResponse или None в случае ошибки
        """

        logger.info(f"Отправлен запрос, request type: {request_type}, url: {url}, body: {json}, other ags: {kwargs}")

        # Инициализируем вне try-except блока, для finally
        response: Optional[aiohttp.ClientResponse] = None

        try:
            # Получаем сессию
            session: ClientSession = await self.get_session()

            # Отправляем запрос в зависимости от его метода
            if request_type == REQUEST_TYPE.GET:
                response = await session.get(url, **kwargs)
            elif request_type == REQUEST_TYPE.POST:
                response = await session.post(url, json=json, **kwargs)
            elif request_type == REQUEST_TYPE.PUT:
                response = await session.put(url, json=json, **kwargs)
            elif request_type == REQUEST_TYPE.DELETE:
                response = await session.delete(url, **kwargs)
            elif request_type == REQUEST_TYPE.PATCH:
                response = await session.patch(url, json=json, **kwargs)

            if response is not None:
                # Заворачиваем в адаптер
                result = APIService.Response(response.status, await response.json())

                logger.info(f'request to url {url} with args {json}, {kwargs} response status: {result.status}')
                return result

        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при отправке запроса: {type(e)} {e.args}, информация по запросу: \
             request type: {request_type.value}, url: {url}, body: {json}, other ags: {kwargs}")

            raise e

        finally:
            # Закрываем соединение
            if response is not None:
                response.close()

    async def endpoint_with_pagination_request(self, url, model: Type[T]) -> PaginationAPIReponse[T]:
        """
        GET запрос на эндпоинт с пагинацией
        Все ответы от сервера на эндпоинты с пагинацией имеют общий вид:

        {"count": ...,
        "next": ...,
        "previous": ...,
        "result": []}

        Достаточно идейно было выделить все запросы на подобные эндпоинты в отдельный метод

        :param url: URL, на который нужно отправить запрос.
        :param model: Модель, в которую будут сериализовываться все объекты из result
        :return: PaginationAPIResponse с полем result типа List[model]
        """

        # Запрос
        response = await self.__make_request(REQUEST_TYPE.GET, url)

        # Сереализация ответа
        json_data = await response.json()
        result_field = []

        for item in json_data["results"]:
            result_field.append(model(**item))

        serialize_response = PaginationAPIReponse(
            count=json_data["count"],
            next=json_data["next"],
            previous=json_data["previous"],
            result=result_field)

        return serialize_response

    async def get_collections(self, url: str) -> PaginationAPIReponse[Collection]:
        """
        Получить коллекции со страницы URL.

        :param url: URL страницы
        :return:
        """

        return await self.endpoint_with_pagination_request(url, Collection)

    async def get_symbols(self, url: str) -> PaginationAPIReponse[Symbol]:
        """
        Получить страницу узоров по указанному URL

        :param url: URL страницы
        :return: ответ в объектной форме
        """

        return await self.endpoint_with_pagination_request(url, Symbol)

    async def get_backdrops(self, url: str) -> PaginationAPIReponse[Backdrop]:
        """
        Получить страницу фонов по указанному URL

        :param url: URL страницы
        :return: ответ в объектной форме
        """

        return await self.endpoint_with_pagination_request(url, Backdrop)

    async def get_models(self, url: str) -> PaginationAPIReponse[Model]:
        """
        Получить страницу моделей по указанному URL

        :param url: URL страницы
        :return: ответ в объектной форме
        """

        return await self.endpoint_with_pagination_request(url, Model)


    async def get_user(self, user_id: int) -> Optional[User]:
        """
        Получить пользователя по user_id

        :param user_id: айди пользователя
        :return: User объект или None если пользователь не найден
        """

        response = await self.__make_request(
            REQUEST_TYPE.GET,
            f"{APIService.HOST}/api/v1/users/{user_id}")

        if response.status == 404:
            logger.warning(f"Попытка получить пользователя {user_id}, завершилась ошибкой 404")
            return None

        json_data = await response.json()
        return User(**json_data)

    async def create_user(self, json: dict) -> None:
        """
        Создать пользователя

        :param json: данные пользователя
        :return: None
        """

        await self.__make_request(
            REQUEST_TYPE.POST,
            f'{APIService.HOST}/api/v1/users/',
            json=json)

    async def get_nfts(
            self,
            collection: Collection,
            model: Model = None,
            backdrop: Backdrop = None,
            symbol: Symbol = None
    ) -> NFTSAPIResponse:
        """
        Получите NFT с сервера по фильтрам

        :param collection: обязательный параметр, название коллекции NFT
        :param model: модель в коллекции NFT
        :param backdrop: фон коллекции NFT
        :param symbol: узор коллекции NFT
        :return: NFTSAPIResponse
        """

        # Формируем параметры запроса
        params = f"?collection={collection.name}"

        if model:
            params += f"&model={model.name}"
        if backdrop:
            params += f"&backdrop={backdrop.name}"
        if symbol:
            params += f"&symbol={symbol.name}"

        # Отправляем запрос
        response = await self.__make_request(
            REQUEST_TYPE.GET,
            f"{APIService.HOST}/api/v1/nfts/{params}"
        )

        # Сериализуем данные

        result = []

        for item in await response.json():
            nft = NFT(
                model=Model(name=item['nft_model']),
                collection=Collection(name=item['collection'], indexed=None, quantity=None),
                backdrop=Backdrop(name=item['backdrop']),
                symbol=Symbol(name=item['symbol']),
                owner=Owner(name=item['owner']),
            )

            result.append(nft)

        serialize_response = NFTSAPIResponse(result)

        return serialize_response

    async def close_session(self) -> None:
        """
        Так как я не использую контекстный менеджер для закрытия aiohttp.ClientSession
        Я закрываю его в main.py при помощи этого метода

        :return: None
        """
        await self.__session.close()
        logger.warning("Сессия успешно закрыта!")
