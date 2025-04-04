from typing import Any, Dict

import allure
from httpx import Client, URL, Response, QueryParams, Headers
from httpx._types import RequestData, RequestFiles

from clients.event_hooks import log_request_event_hook, log_response_event_hook
from config import HTTPClientConfig


class BaseClient:
    """
    Базовый клиент для выполнения HTTP-запросов.

    Этот класс предоставляет основные методы для выполнения HTTP-запросов 
    (GET, POST, PATCH, DELETE) и использует httpx.Client для выполнения 
    запросов. Каждый метод добавлен с использованием allure для генерации 
    отчетов о тестах.
    """

    def __init__(self, client: Client):
        """
        Инициализация клиента.
        :param client: Экземпляр httpx.Client
        """
        self.client = client
        self._auth_token = 1234567890

    def set_auth_token(self, token: str) -> None:
        """
        Устанавливает Bearer токен для авторизации.
        
        :param token: JWT токен авторизации
        """
        self._auth_token = token

    def _get_auth_headers(self) -> Dict[str, str]:
        """
        Формирует заголовки авторизации.
        
        :return: Словарь с заголовками авторизации
        """
        headers = {}
        if self._auth_token:
            headers["Authorization"] = f"Bearer {self._auth_token}"
        return headers

    @allure.step("Make GET request to {url}")
    def get(self, url: URL | str, params: QueryParams | None = None, headers: Headers | None = None) -> Response:
        """
        Выполняет GET-запрос.

        :param url: URL эндпоинта
        :param params: Query параметры запроса
        :param headers: Дополнительные заголовки запроса
        :return: HTTP-ответ
        """
        all_headers = {**self._get_auth_headers(), **(headers or {})}
        return self.client.get(url, params=params, headers=all_headers)

    @allure.step("Make POST request to {url}")
    def post(
            self,
            url: URL | str,
            json: Any | None = None,
            data: RequestData | None = None,
            files: RequestFiles | None = None,
            headers: Headers | None = None
    ) -> Response:
        """
        Выполняет POST-запрос.

        :param url: URL эндпоинта
        :param json: JSON тело запроса
        :param data: Данные формы
        :param files: Файлы для загрузки
        :param headers: Дополнительные заголовки запроса
        :return: HTTP-ответ
        """
        all_headers = {**self._get_auth_headers(), **(headers or {})}
        return self.client.post(url, json=json, data=data, files=files, headers=all_headers)

    # @allure.step("Make PATCH request to {url}")
    # def patch(self, url: URL | str, json: Any | None = None) -> Response:
    #     return self.client.patch(url, json=json)

    # @allure.step("Make DELETE request to {url}")
    # def delete(self, url: URL | str) -> Response:
    #     return self.client.delete(url)


def get_http_client(config: HTTPClientConfig) -> Client:
    return Client(
        timeout=config.timeout,
        base_url=config.client_url,
        event_hooks={
            "request": [log_request_event_hook],
            "response": [log_response_event_hook]
        },
    )
