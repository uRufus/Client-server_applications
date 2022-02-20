import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))

from server import process_client_message
from common.variables import ACTION, ACCOUNT_NAME, PRESENCE, TIME, USER, DEFAULT_ACCOUNT_NAME, \
    OK_DICT, ERROR_DICT_SERVER


class TestClass(unittest.TestCase):
    def setUP(self):
        pass

    def tearDown(self):
        pass

    def test_process_client_message_200(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME}}), OK_DICT)

    def test_process_client_message_400(self):
        self.assertEqual(process_client_message({USER: {ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME}}), ERROR_DICT_SERVER)

    def test_dict_client_message_200(self):
        self.assertIsInstance(process_client_message(
            {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME}}), dict)

    def test_dict_client_message_400(self):
        self.assertIsInstance(process_client_message({USER: {ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME}}), dict)

    def test_no_str_client_message_200(self):
        self.assertNotIsInstance(process_client_message(
            {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME}}), str)

    def test_no_str_client_message_400(self):
        self.assertNotIsInstance(process_client_message({ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME}), str)


if __name__ == '__main__':
    unittest.main()
