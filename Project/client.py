"""
Функции клиента: сформировать presence-сообщение; отправить сообщение серверу;
получить ответ сервера; разобрать сообщение сервера;параметры командной
строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера;
port — tcp-порт на сервере, по умолчанию 7777.
"""
import argparse
import logging
import logs.client_log_config
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv, exit
import json
from time import time
from decos import log
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, \
    DEFAULT_ACCOUNT_NAME, DEFAULT_IP_ADDRESS, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_msg, send_msg, check_port

# Инициализация логирования клиента
CLIENT_LOGGER = logging.getLogger('client')


@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                           f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def create_msg(sock, account_name='Guest'):

    msg = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if msg == '!!!':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        exit(0)
    msg_dict = {
        ACTION: MESSAGE,
        TIME: time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: msg
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {msg_dict}')
    return msg_dict

@log
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def process_ans(message):
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера : {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : ok'
        elif message[RESPONSE] == 400:
            return f'400 : {message[ERROR]}'
    raise ValueError


@log
def arg_parser():
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='send', nargs='?')
    namespace = parser.parse_args(argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode
    check_port(server_port)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, '
                        f'допустимые режимы: listen , send')
        exit(1)

    return server_address, server_port, client_mode


def main():
    server_address, server_port, client_mode = arg_parser()
    CLIENT_LOGGER.info(f'Запущен клиент с параметрами: адрес сервера : {server_address}, порт : {server_port}')
    try:
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_msg(transport, create_presence())
        answer = process_ans(get_msg(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error(f'Не удалось декодировать Json строку')
        exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}')
        exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    send_msg(transport, create_msg(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    message_from_server(get_msg(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    exit(1)


if __name__ == '__main__':
    main()
