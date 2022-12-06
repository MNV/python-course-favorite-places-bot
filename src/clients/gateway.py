"""
Функции для взаимодействия с внешним сервисом-провайдером данных о местонахождении.
"""
from typing import Optional

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from graphql import DocumentNode

from clients.base.base import BaseClient
from clients.shemas import PlaceDTO
from settings import settings


class GatewayClient(BaseClient):
    """
    Реализация функций для взаимодействия с GraphQL-шлюзом.
    """

    @property
    def base_url(self) -> str:
        return settings.gateway_url

    def _request(self, query: DocumentNode, variables: Optional[dict] = None) -> dict:
        # конфигурация транспорта данных
        transport = RequestsHTTPTransport(
            url=self.base_url,
            verify=True,
            retries=3,
        )
        # инициализация клиента для взаимодействия с GraphQL
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # выполнение запроса и возврат результата
        return client.execute(query, variable_values=variables)

    def get_place(self, place_id: str) -> Optional[PlaceDTO]:
        """
        Получение объекта любимого места по его идентификатору.

        :param place_id: Идентификатор места.
        :return:
        """

        # формирование GraphQL-запроса
        query = gql(
            """
            query getPlace($placeId: ID!) {
                place(placeId: $placeId) {
                    id
                    latitude
                    longitude
                    description
                    city
                    locality
                }
            }
            """
        )
        variables = {"placeId": place_id}
        if response := self._request(query, variables=variables):
            # todo: добавить обработку исключений
            item = response["place"]

            return PlaceDTO(
                id=item.get("id"),
                latitude=item.get("latitude"),
                longitude=item.get("longitude"),
                description=item.get("description"),
                city=item.get("city"),
                locality=item.get("locality"),
            )

        return None

    def get_places(self) -> Optional[list[PlaceDTO]]:
        """
        Получение списка любимых мест.

        :return:
        """

        # формирование GraphQL-запроса
        query = gql(
            """
            query {
                places {
                    id
                    latitude
                    longitude
                    description
                    city
                    locality
                }
            }
            """
        )

        if response := self._request(query):
            places = response.get("places", [])
            items = []
            for item in places:
                items.append(
                    PlaceDTO(
                        id=item.get("id"),
                        latitude=item.get("latitude"),
                        longitude=item.get("longitude"),
                        description=item.get("description"),
                        city=item.get("city"),
                        locality=item.get("locality"),
                    )
                )
            return items

        return None

    def create(self, latitude: float, longitude: float, description: str) -> bool:
        """
        Создание нового объекта любимого места.

        :param latitude: Широта.
        :param longitude: Долгота.
        :param description: Описание.
        :return:
        """

        # формирование GraphQL-запроса
        query = gql(
            """
            mutation createPlace($latitude: Float!, $longitude: Float!, $description: String!) {
                createPlace(latitude: $latitude, longitude: $longitude, description: $description) {
                    result
                }
            }
            """
        )
        variables = {
            "latitude": latitude,
            "longitude": longitude,
            "description": description,
        }
        if response := self._request(query, variables=variables):
            # todo: добавить обработку исключений
            result = response.get("createPlace", {}).get("result")

            return result

        return False

    def delete(self, place_id: str) -> bool:
        """
        Удаление объекта любимого места по его идентификатору.

        :param place_id: Идентификатор места.
        :return:
        """

        # формирование GraphQL-запроса
        query = gql(
            """
            mutation deletePlace($placeId: Int!) {
                deletePlace(placeId: $placeId) {
                    result
                }
            }
            """
        )
        variables = {"placeId": place_id}
        if response := self._request(query, variables=variables):
            # todo: добавить обработку исключений
            result = response.get("deletePlace", {}).get("result")

            return result

        return False
