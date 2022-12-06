from telegram import InlineKeyboardButton

from menu.base import BaseMenu


class PlacesMenu(BaseMenu):
    """
    Функции меню для списка любимых мест.
    """

    def build_menu(
        self, buttons: list[InlineKeyboardButton], cols_count: int
    ) -> list[list[InlineKeyboardButton]]:
        """
        Формирование меню на основе переданной конфигурации.

        :param buttons: Список объектов кнопок.
        :param cols_count: Количество колонок.
        :return:
        """

        return super().build_menu(buttons, 1)


class PlaceMenu(BaseMenu):
    """
    Функции меню для работы с объектом любимого места.
    """

    def __init__(self, buttons: dict[str, str]):
        super().__init__()

        self.default_buttons = buttons
