from abc import ABC, abstractmethod
from typing import Any

from telegram import Update


class CommandHandler(ABC):
    """
    Обработчик команд от пользователя.
    """

    @abstractmethod
    def handle(self, update: Update, **kwargs: Any) -> None:
        """
        Обработка команды.

        :param update: Объект с данными, поступившими от чат-бота.
        :return:
        """
