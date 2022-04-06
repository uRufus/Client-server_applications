"""Программа-лаунчер"""

import subprocess

processes = []

while True:
    action = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if action == 'q':
        break
    elif action == 's':
        clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
        processes.append(subprocess.Popen('python server.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(clients_count):
            processes.append(subprocess.Popen(f'python client.py -n test{i + 1}',
                                              creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif action == 'x':
        while processes:
            processes.pop().kill()
