import json
from .variables import MAX_PACKAGE_LENGTH, ENCODING
from sys import exit


def check_port(port):
    try:
        if port < 1024 or port > 65535:
            raise ValueError
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        exit(1)


def check_instance(variable, types):
    try:
        if not isinstance(variable, types):
            raise ValueError
    except ValueError:
        print(f'Значение {variable} не является типом {types}')
        exit(1)


def send_msg(sock, msg):
    check_instance(msg, dict)
    js_msg = json.dumps(msg)
    check_instance(js_msg, str)
    encoded_msg = js_msg.encode(ENCODING)
    check_instance(encoded_msg, bytes)
    sock.send(encoded_msg)


def get_msg(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    check_instance(encoded_response, bytes)
    json_response = encoded_response.decode(ENCODING)
    check_instance(json_response, str)
    response = json.loads(json_response)
    check_instance(response, dict)
    return response
