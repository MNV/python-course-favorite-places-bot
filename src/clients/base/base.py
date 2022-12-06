"""
Базовые функции для клиентов внешних сервисов.
"""

from abc import ABC, abstractmethod
from typing import Any, Union

from graphql import DocumentNode, ExecutionResult


class BaseClient(ABC):
    """
    Базовый класс, реализующий интерфейс для клиентов.
    """

    @property
    @abstractmethod
    def base_url(self) -> str:
        """
        Получение базового URL для запросов.

        :return:
        """

    @abstractmethod
    def _request(self, query: DocumentNode) -> Union[dict[str, Any], ExecutionResult]:
        """
        Формирование и выполнение запроса.

        :param query: Запрос для выполнения.
        :return:
        """
