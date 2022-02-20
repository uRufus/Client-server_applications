"""
Функции сервера: принимает сообщение клиента; формирует ответ клиенту;
отправляет ответ клиенту; имеет параметры командной строки: -p <port> — TCP-порт
для работы (по умолчанию использует 7777); -a <addr> — IP-адрес для прослушивания (по умолчанию слушает
все доступные адреса).
"""
import logging
import logs.server_log_config
from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM
import json
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESSSE, DEFAULT_ACCOUNT_NAME
from common.utils import get_msg, send_msg, check_port

# Инициализация логирования сервера
SERVER_LOGGER = logging.getLogger('server')


def process_client_message(message):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == DEFAULT_ACCOUNT_NAME:
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESSSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in argv:
            listen_port = int(argv[argv.index('-p') + 1])
            SERVER_LOGGER.info(f'Слушаем порт : {listen_port}')
        else:
            listen_port = DEFAULT_PORT
            SERVER_LOGGER.info(f'Слушаем порт по умолчанию : {listen_port}')
        check_port(listen_port)
    except IndexError:
        SERVER_LOGGER.critical('После параметра \'-p\' необходимо указать номер порта.')
        exit(1)

    try:
        if '-a' in argv:
            listen_address = argv[argv.index('-a') + 1]
            SERVER_LOGGER.info(f'Слушаем адрес : {listen_address}')
        else:
            listen_address = ''
            SERVER_LOGGER.info(f'Слушаем все адреса')
    except IndexError:
        SERVER_LOGGER.critical('После параметра \'-a\' необходимо указать IP-адрес.')
        exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'Установлено соединение с ПК : {client_address}')
        try:
            message_from_client = get_msg(client)
            SERVER_LOGGER.debug(f'Получено сообщение от клиента : {message_from_client}')
            response = process_client_message(message_from_client)
            SERVER_LOGGER.info(f'Сформирован ответ клиенту : {response}')
            send_msg(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается')
            client.close()
        # except (ValueError, json.JSONDecodeError):
        #     print('Принято некорректное сообщение от клиента.')
        #     client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать Json строку, полученную от'
                                f'клиента {client_address}. Соединение закрывается')
            client.close()


if __name__ == '__main__':
    main()
