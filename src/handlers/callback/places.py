from telegram import CallbackQuery, ParseMode

from clients.gateway import GatewayClient
from clients.shemas import PlaceDTO
from menu.places import PlaceMenu


class PlaceCallbackHandler:
    """
    Обработка функций обратного вызова для управления данными о конкретном любимом месте.
    """

    def handle(self, callback_query: CallbackQuery) -> bool:
        """
        Обработка обратного вызова.

        :param callback_query: Объект запроса обратного вызова.
        :return:
        """

        query_data = callback_query.data
        # получение идентификатора любимого места
        place_id = query_data.split(":")[1]
        # получение информации о месте
        place = GatewayClient().get_place(place_id)

        if place:
            # отправка данных о месте в чат-бот
            callback_query.edit_message_text(
                text=self.__build_message(place), parse_mode=ParseMode.MARKDOWN
            )

            # формирование inline-меню
            reply_markup = PlaceMenu(
                buttons={
                    "Редактировать": f"place.edit:{place_id}",
                    "Удалить": f"place.delete:{place_id}",
                }
            ).get_menu()
            callback_query.edit_message_reply_markup(reply_markup=reply_markup)

            callback_query.answer(
                text="Информация о любимом месте.",
            )
        else:
            # todo: обработать исключительную ситуацию с логированием
            callback_query.answer("Любимое место не найдено.")

        return True

    def __build_message(self, place: PlaceDTO) -> str:
        """
        Формирование описания объекта любимого места.

        :param place: Объект с данными места.
        :return:
        """

        return (
            f"*Город:* `{place.city}`\n"
            f"*Местность:* `{place.locality}`\n"
            f"*Координаты:* `{place.latitude}°, {place.longitude}°`\n"
            f"*Мой комментарий:* {place.description}\n\n"
        )


class PlaceDeleteCallbackHandler:
    """
    Обработка функций обратного вызова для удаления мест.
    """

    def handle(self, callback_query: CallbackQuery) -> bool:
        """
        Обработка обратного вызова.

        :param callback_query: Объект запроса обратного вызова.
        :return:
        """

        query_data = callback_query.data
        # получение идентификатора любимого места
        place_id = query_data.split(":")[1]
        # удаление объекта места
        result = GatewayClient().delete(place_id)

        if result:
            callback_query.edit_message_text(text="Любимое место было удалено.")
            callback_query.answer(
                text="Успешно удалено.",
            )
        else:
            # todo: обработать исключительную ситуацию с логированием
            callback_query.answer("Ошибка при удалении.")

        return True
