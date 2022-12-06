from typing import Any

from telegram import Chat, Update

from clients.gateway import GatewayClient
from handlers.command.base import CommandHandler
from menu.places import PlacesMenu


class PlacesCommandHandler(CommandHandler):
    """
    Обработчик команды `/places`.
    """

    def handle(self, update: Update, **kwargs: Any) -> None:
        """
        Получение списка любимых мест.

        :param update: Объект с данными, поступившими от чат-бота.
        :return:
        """

        places = GatewayClient().get_places()

        menu = PlacesMenu()
        buttons = {
            f"{place.city} ({place.locality})": f"place:{place.id}" for place in places
        }
        reply_markup = menu.set_buttons(buttons).get_menu()

        if isinstance(update.effective_chat, Chat):
            update.effective_chat.send_message(
                text="Мои любимые места:", reply_markup=reply_markup
            )
