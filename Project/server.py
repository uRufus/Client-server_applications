"""
Функции сервера: принимает сообщение клиента; формирует ответ клиенту;
отправляет ответ клиенту; имеет параметры командной строки: -p <port> — TCP-порт
для работы (по умолчанию использует 7777); -a <addr> — IP-адрес для прослушивания (по умолчанию слушает
все доступные адреса).
"""
from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM
import json
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESSSE
from common.utils import get_msg, send_msg, check_port


def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESSSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in argv:
            listen_port = int(argv[argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        check_port(listen_port)
    except IndexError:
        print('После параметра \'-p\' необходимо указать номер порта.')
        exit(1)

    try:
        if '-a' in argv:
            listen_address = argv[argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        print('После параметра \'-a\' необходимо указать IP-адрес.')
        exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_msg(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_msg(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорректное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
