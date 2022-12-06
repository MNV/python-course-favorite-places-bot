"""
Функции взаимодействия с API Telegram.
"""
import logging

from telegram import (
    Bot,
    Chat,
    ParseMode,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
    Handler,
    MessageHandler,
    Updater,
)
from telegram.ext.utils.types import CCT

from handlers.callback.places import PlaceCallbackHandler, PlaceDeleteCallbackHandler
from handlers.command.places import PlacesCommandHandler
from handlers.message.places import PlaceAddMessageHandler
from settings import settings

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ChatBotTelegram:
    """
    Чат-бот для Telegram.
    """

    # команды чат-бота
    KEYBOARD_COMMANDS = {
        "places": "🧭 Список мест",
        "add": "📌 Добавить место",
        "help": "ℹ Техподдержка",
    }

    # значение состояния для запроса местоположения
    STATE_LOCATION = 1
    # значение состояния для запроса описания
    STATE_DESCRIPTION = 2

    def __init__(self, updater_object: Updater):
        """
        Конструктор.

        :param updater_object: Объект для получения обновлений (сообщений пользователя) от чат-бота.
        """

        self.updater = updater_object

    def add_handler(self, handler: Handler[Update, CCT]) -> None:
        """
        Добавление обработчиков команд от пользователя чат-бота.

        :param handler: Обработчик команд.
        :return:
        """

        self.updater.dispatcher.add_handler(handler)  # type: ignore

    def start(self) -> None:
        """
        Запуск функций взаимодействия с Telegram
        для получения обновлений (сообщений от пользователя) и их обработки.

        :return:
        """

        self.updater.start_polling()
        self.updater.idle()

    def command_start(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> None:
        """
        Обработка команды `/start`.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        if isinstance(update.effective_chat, Chat):
            keyboard_buttons = [
                [
                    self.KEYBOARD_COMMANDS["places"],
                    self.KEYBOARD_COMMANDS["add"],
                ],
                [self.KEYBOARD_COMMANDS["help"]],
            ]
            keyboard = ReplyKeyboardMarkup(
                keyboard=keyboard_buttons, resize_keyboard=True
            )

            update.effective_chat.send_message(
                text=f"Добро пожаловать, {update.message.chat.first_name}!" + "\n\n"
                "Желаем приятного пользования сервисом.\n\n"
                'Список команд бота раскрывается при вводе символа "/".\n'
                "Также команды доступны в основном кнопочном меню бота.\n\n"
                "/help - руководство пользователя.\n",
                reply_markup=keyboard,
            )

    def command_places(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> None:
        """
        Обработка команды `/places`.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        PlacesCommandHandler().handle(update)

    def command_add(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> int:
        """
        Обработка команды `/add`.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        update.message.reply_text("Пожалуйста, отправьте ваше местоположение:")

        return self.STATE_LOCATION

    def command_help(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> None:
        """
        Обработка команды `/help`.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        update.effective_chat.send_message(  # type: ignore
            text="По вопросам работы сервиса и техподдержки направляйте, пожалуйста, "
            "сообщения пользователю @MichaelNV.\n\n"
            "Будем рады вашим предложениям и пожеланиям!\n\n",
            parse_mode=ParseMode.HTML,
        )

    def cancel(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> int:
        """
        Завершение взаимодействия с чат-ботом.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        update.message.reply_text(
            "Спасибо, что обратились к нашему сервису.",
            reply_markup=ReplyKeyboardRemove(),
        )

        return ConversationHandler.END

    @staticmethod
    def message_unknown(
        update: Update, context: CallbackContext  # pylint: disable=unused-argument
    ) -> None:
        """
        Обработка неизвестного чат-боту текстового сообщения.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        update.effective_chat.send_message(  # type: ignore
            text="Пока не очень понимаю что имелось в виду.\n\n"
            'Список доступных команд раскрывается при вводе символа "/".\n'
            "Техподдержка – /help.\n",
        )

    def callback_place(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> None:
        """
        Обработка запроса на просмотр объекта любимого места.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        PlaceCallbackHandler().handle(update.callback_query)

    def callback_place_delete(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> None:
        """
        Обработка запроса на удаление объекта любимого места.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        PlaceDeleteCallbackHandler().handle(update.callback_query)

    def text_message_handler(self, update: Update, context: CallbackContext) -> None:
        """
        Обработка текстовых сообщений от пользователя.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        keyboard_commands = {
            value: key for key, value in self.KEYBOARD_COMMANDS.items()
        }
        # поиск команды и её выполнение
        if command_name := keyboard_commands.get(update.message.text):
            if method := getattr(self, "command_" + command_name):
                return method(update, context)

            return None

        # обработка неизвестной команды
        return self.message_unknown(update, context)

    def message_location(self, update: Update, context: CallbackContext) -> int:
        """
        Обработка текстовых сообщений от пользователя.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        if isinstance(context.user_data, dict):
            context.user_data["location"] = update.message.location

        update.message.reply_text("Добавьте описание для места: ")

        return self.STATE_DESCRIPTION

    def message_description(self, update: Update, context: CallbackContext) -> int:
        """
        Обработка текстовых сообщений от пользователя.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        if context.user_data and "location" in context.user_data:
            PlaceAddMessageHandler().handle(
                update,
                location=context.user_data["location"],
                description=update.message.text,
            )
        # todo: обработать исключительную ситуацию

        return ConversationHandler.END


try:
    updater = Updater(
        bot=Bot(settings.chatbot_telegram.api_token),
    )
    bot = ChatBotTelegram(updater)

    # обработка команд
    bot.add_handler(CommandHandler("start", bot.command_start))
    bot.add_handler(CommandHandler("places", bot.command_places))
    bot.add_handler(CommandHandler("help", bot.command_help))

    # обработка команды для создания нового объекта любимого места
    bot.add_handler(
        ConversationHandler(
            # обработка функций обратного вызова
            # self.KEYBOARD_COMMANDS
            entry_points=[
                CommandHandler("add", bot.command_add),
                MessageHandler(
                    Filters.regex(f'^{bot.KEYBOARD_COMMANDS.get("add")}$'),
                    bot.command_add,
                ),
            ],
            states={
                bot.STATE_LOCATION: [
                    # обработка сообщения, содержащего сведения о локации
                    MessageHandler(Filters.location, bot.message_location),
                ],
                bot.STATE_DESCRIPTION: [
                    # обработка сообщения, содержащего описание места
                    MessageHandler(Filters.text, bot.message_description),
                ],
            },
            fallbacks=[CommandHandler("cancel", bot.cancel)],
        )
    )

    # обработка функций обратного вызова
    # просмотр объекта
    bot.add_handler(CallbackQueryHandler(bot.callback_place, pattern=r"place:\d{1,20}"))
    # удаление объекта
    bot.add_handler(
        CallbackQueryHandler(
            bot.callback_place_delete, pattern=r"place.delete:\d{1,20}"
        )
    )

    # обработка текстовых сообщений (кнопочного меню или любого текста)
    bot.add_handler(MessageHandler(Filters.text, bot.text_message_handler))

    # запуск взаимодействия с чат-ботом
    bot.start()

except Exception as exception:
    # todo: реализовать обработку исключений
    raise exception
