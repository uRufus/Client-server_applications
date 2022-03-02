"""Константы"""


DEFAULT_PORT = 7777

DEFAULT_IP_ADDRESS = '127.0.0.1'

MAX_CONNECTIONS = 5

MAX_PACKAGE_LENGTH = 1024

ENCODING = 'utf-8'

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
DEFAULT_ACCOUNT_NAME = 'Kitty'
SENDER = 'sender'


PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
RESPONDEFAULT_IP_ADDRESSSE = 'respondefault_ip_addressse'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'

# For tests
OK_DICT = {RESPONSE: 200}
ERROR_DICT = {RESPONSE: 400, ERROR: 'Bad Request'}
ERROR_DICT_SERVER = {ERROR: 'Bad Request', RESPONDEFAULT_IP_ADDRESSSE: 400}
DICT_SEND = {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME}}