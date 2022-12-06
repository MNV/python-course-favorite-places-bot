Установка
=========

Установите требуемое ПО:

1. Docker для контейнеризации – |link_docker|

.. |link_docker| raw:: html

   <a href="https://www.docker.com" target="_blank">Docker Desktop</a>

2. Для работы с системой контроля версий – |link_git|

.. |link_git| raw:: html

   <a href="https://github.com/git-guides/install-git" target="_blank">Git</a>

3. IDE для работы с исходным кодом – |link_pycharm|

.. |link_pycharm| raw:: html

    <a href="https://www.jetbrains.com/ru-ru/pycharm/download" target="_blank">PyCharm</a>

Клонируйте репозиторий проекта в свою рабочую директорию:

    .. code-block:: console

        git@github.com:mnv/python-course-references-bot.git

Использование
-------------

Перед началом использования приложения необходимо его сконфигурировать.

.. note::

    Для конфигурации выполните команды, описанные ниже, находясь в корневой директории проекта (на уровне с директорией `src`).

1. Скопируйте файл настроек `.env.sample`, создав файл `.env`:
    .. code-block:: console

        cp .env.sample .env

    Этот файл содержит преднастроенные переменные окружения, значения которых будут общими для всего приложения.
    Файл примера (`.env.sample`) содержит набор переменных со значениями по умолчанию.
    Созданный файл `.env` можно настроить в зависимости от окружения.

    .. warning::

        Никогда не добавляйте в систему контроля версий заполненный файл `.env` для предотвращения компрометации информации о конфигурации приложения.

2. Соберите Docker-контейнеры с помощью Docker Compose:
    .. code-block:: console

        docker compose build

    Данную команду необходимо выполнять повторно в случае обновления зависимостей в файле `requirements.txt`.

3. Для запуска приложения выполните:
    .. code-block:: console

        docker compose up

Настройка чат-бота
------------------

Чтобы начать работу с чат-ботом, его необходимо зарегистрировать в Telegram (https://core.telegram.org/bots/tutorial#getting-ready).
После регистрации вы получите токен доступа, который нужно назначить переменной окружения `CHATBOT_TELEGRAM__API_TOKEN`.

Затем с помощью Bot Father нужно создать команды для чат-бота:
    - `/places` (для получения списка любимых мест)
    - `/add` (для добавления нового любимого места)
    - `/help` (для техподдержки пользователей)

Подробнее можно узнать по ссылке — https://core.telegram.org/bots/tutorial#executing-commands.

После этого запустите сервис:
    .. code-block:: console

        docker compose up

Затем перейдите к чат-боту и вызовите какую-либо команду.
Сервис должен принять данные от Telegram, обработать их и отправить ответ чат-боту.

Зависимости
-----------

Этот проект является частью микросервисного проекта, состоящего из сервисов:

- `Countries Informer Service <https://github.com/mnv/python-course-countries-informer>`_
- `Favorite Places Service <https://github.com/mnv/python-course-favorite-places>`_
- `GraphQL API Gateway <https://github.com/mnv/python-course-graphql-gateway>`_

Чат-бот взаимодействует только с GraphQL-шлюзом, который вызывает другие микросервисы для управления данными.
Поэтому перед запуском чат-бота вам нужно запустить эти сервисы, используя их руководство.

Автоматизация
-------------

Проект содержит специальный файл (`Makefile`) для автоматизации выполнения команд:

1. Сборка Docker-контейнеров:
    .. code-block:: console

        make build

2. Сборка документации Sphinx:
    .. code-block:: console

        make docs-html

3. Форматирование кода:
    .. code-block:: console

        make format

4. Статический анализ кода:
    .. code-block:: console

        make lint

5. Запуск автотестов:
    .. code-block:: console

        make test

6. Запуск всех функций поддержки качества кода (format, lint, test):
    .. code-block:: console

        make all
