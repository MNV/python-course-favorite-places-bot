import logging

from telegram import Location, Update

from clients.gateway import GatewayClient

logger = logging.getLogger()


class PlaceAddMessageHandler:
    """
    Функции для обработки запросов для создания нового объекта любимого места.
    """

    def handle(self, update: Update, location: Location, description: str) -> None:
        """
        Обработка события загрузки файла.

        :param update: Объект с данными, поступившими от чат-бота.
        :param location: Объект с данными о местоположении.
        :param description: Описание добавляемого места.
        :return:
        """

        result = GatewayClient().create(
            latitude=location.latitude,
            longitude=location.longitude,
            description=description,
        )
        if result:
            update.message.reply_text("Место добавлено.")
        else:
            # todo: добавить обработку исключительных ситуаций с логированием
            update.message.reply_text("Место не было добавлено.")
