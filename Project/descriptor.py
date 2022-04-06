import logging
logger = logging.getLogger('server_dist')


class CheckPort:
    '''Класс для проверки корректности порта'''
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(
                f'Попытка запуска сервера с указанием неподходящего порта {value}. '
                f'Порт не может быть меньше 1023 или больше 65536.')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name