# Favorite Places Bot

Chatbot to manage your favorite places.

## Requirements:

Install the appropriate software:

1. [Docker Desktop](https://www.docker.com).
2. [Git](https://github.com/git-guides/install-git).
3. [PyCharm](https://www.jetbrains.com/ru-ru/pycharm/download) (optional).

## Installation

Clone the repository to your computer:
```bash
git clone https://github.com/mnv/python-course-favorite-places-bot
```

1. To configure the application copy `.env.sample` into `.env` file:
    ```shell
    cp .env.sample .env
    ```
   
    This file contains environment variables that will share their values across the application.
    The sample file (`.env.sample`) contains a set of variables with default values. 
    So it can be configured depending on the environment.

2. Build the container using Docker Compose:
    ```shell
    docker compose build
    ```
    This command should be run from the root directory where `Dockerfile` is located.
    You also need to build the docker container again in case if you have updated `requirements.txt`.

3. To run the project inside the Docker container:
    ```shell
    docker compose up
    ```

## Usage

### Chatbot

To start working with a chatbot, you need to register it in Telegram ([https://core.telegram.org/bots/tutorial#getting-ready](https://core.telegram.org/bots/tutorial#getting-ready)). 
After registration, you will receive an access token, which must be set to an environment variable `CHATBOT_TELEGRAM__API_TOKEN`.

Then, using Bot Father you need to create commands for the chatbot:

    - /places
    - /add
    - /help

More details can be found at the link – [https://core.telegram.org/bots/tutorial#executing-commands](https://core.telegram.org/bots/tutorial#executing-commands).

After that you can start the service:

```shell
docker compose up
```

Then proceed to the chatbot and call a command. The service should accept data from Telegram, process it and send the response to the chatbot.

### Dependencies

This project is a part of a microservices project consisting of:

- [Countries Informer Service](https://github.com/mnv/python-course-countries-informer)
- [Favorite Places Service](https://github.com/mnv/python-course-favorite-places)
- [GraphQL API Gateway](https://github.com/mnv/python-course-graphql-gateway)

Chatbot interacts only with GraphQL API Gateway which calls other microservices to manage data. 
So before starting a chatbot you need to start those services using their guidance.

### Automation commands

The project contains a special `Makefile` that provides shortcuts for a set of commands:
1. Build the Docker container:
    ```shell
    make build
    ```

2. Generate Sphinx documentation run:
    ```shell
    make docs-html
    ```

3. Autoformat source code:
    ```shell
    make format
    ```

4. Static analysis (linters):
    ```shell
    make lint
    ```

5. Autotests:
    ```shell
    make test
    ```

    The test coverage report will be located at `src/htmlcov/index.html`. 
    So you can estimate the quality of automated test coverage.

6. Run autoformat, linters and tests in one command:
    ```shell
    make all
    ```

Run these commands from the source directory where `Makefile` is located.

## Documentation

The project integrated with the [Sphinx](https://www.sphinx-doc.org/en/master/) documentation engine. 
It allows the creation of documentation from source code. 
So the source code should contain docstrings in [reStructuredText](https://docutils.sourceforge.io/rst.html) format.

To create HTML documentation run this command from the source directory where `Makefile` is located:
```shell
make docs-html
```

After generation documentation can be opened from a file `docs/build/html/index.html`.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
