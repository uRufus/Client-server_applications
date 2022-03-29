"""1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов. 
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или 
ip-адресом. В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения 
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции 
ip_address(). (Внимание! Аргументом сабпроцеса должен быть список, а не строка!!! Крайне желательно использование 
потоков.) """
import platform
import subprocess
import threading
from ipaddress import ip_address
from pprint import pprint

result = {'Доступные узлы': [], 'Недоступные узлы': []}  # словарь с результатами


def check_ip_address(address):
    try:
        ipv4 = ip_address(address)
    except ValueError:
        raise Exception(f'Получен некорректный ip адресс {ipv4}')
    return ipv4


def ping(ipv4, result, get_list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    response = subprocess.Popen(["ping", param, '1', '-w', '1', str(ipv4)],
                                stdout=subprocess.PIPE)
    if response.wait() == 0:
        result["Доступные узлы"].append(str(ipv4))
        res = f"{ipv4} - Узел доступен"
    else:
        result["Недоступные узлы"].append(str(ipv4))
        res = f"{str(ipv4)} - Узел недоступен"

    if not get_list:  # если результаты не надо добавлять в словарь, значит отображаем
        print(res)
    return res


def host_ping(hosts_list, get_list=False):
    threads = []
    for host in hosts_list:
        try:
            ipv4 = check_ip_address(host)
        except Exception as e:
            print(f'{host} - {e} воспринимаю как доменное имя')
            ipv4 = host

        thread = threading.Thread(target=ping, args=(ipv4, result, get_list), daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if get_list:  # если требуется вернуть словарь (для задачи №3), то возвращаем
        return result


if __name__ == '__main__':
    # список проверяемых хостов
    example_list = ['192.168.8.1', '8.8.8.8', 'yandex.ru', 'google.com',
                  '0.0.0.1', '0.0.0.2', '0.0.0.3', '0.0.0.4', '0.0.0.5',
                  '0.0.0.6', '0.0.0.7', '0.0.0.8', '0.0.0.9', '0.0.1.0']
    host_ping(example_list, get_list=True)
    pprint(result)

