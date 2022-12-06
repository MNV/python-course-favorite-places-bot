from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class BaseMenu:
    """
    Базовые функции для формирования меню.
    """

    buttons: dict[str, str] = {}
    default_buttons: dict[str, str] = {}

    def set_buttons(self, items: dict[str, str]) -> "BaseMenu":
        """
        Назначение кнопок для меню.

        :param items: Кнопки.
        :return:
        """

        self.buttons = items

        return self

    def get_menu(self) -> InlineKeyboardMarkup:
        """
        Получение сформированного меню.
        :return:
        """

        return self.build_buttons(self.buttons)

    def build_buttons(self, buttons: dict[str, str]) -> InlineKeyboardMarkup:
        """
        Формирование меню.

        :param buttons:
        :return:
        """

        menu_buttons = self.default_buttons.copy()
        if buttons:
            extra_buttons = self.buttons.copy()
            extra_buttons.update(menu_buttons)
            menu_buttons = extra_buttons

        button_list = []
        for title, callback in menu_buttons.items():
            button_list.append(InlineKeyboardButton(title, callback_data=callback))

        return InlineKeyboardMarkup(self.build_menu(buttons=button_list, cols_count=2))

    def build_menu(
        self, buttons: list[InlineKeyboardButton], cols_count: int
    ) -> list[list[InlineKeyboardButton]]:
        """
        Формирование меню на основе переданной конфигурации.

        :param buttons: Список объектов кнопок.
        :param cols_count: Количество колонок.
        :return:
        """

        return [
            buttons[i : i + cols_count]  # noqa: E203
            for i in range(0, len(buttons), cols_count)
        ]
