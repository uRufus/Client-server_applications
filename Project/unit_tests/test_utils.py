import sys
import os
import unittest
import json

sys.path.append(os.path.join(os.getcwd(), '..'))

from common.utils import check_port, check_instance, send_msg, get_msg
from common.variables import OK_DICT, ERROR_DICT, DICT_SEND, ENCODING


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.received_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestClass(unittest.TestCase):
    def setUP(self):
        pass

    def tearDown(self):
        pass

    def test_check_port(self):
        self.assertIs(check_port(2000), None)

    def test_check_instance(self):
        self.assertIs(check_instance(200, int), None)

    def test_send_msg_ok(self):
        test_socket = TestSocket(DICT_SEND)
        send_msg(test_socket, DICT_SEND)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)

    def test_bytes_send_msg(self):
        test_socket = TestSocket(DICT_SEND)
        send_msg(test_socket, DICT_SEND)
        self.assertIsInstance(test_socket.encoded_message, bytes)

    def test_no_dict_send_msg(self):
        test_socket = TestSocket(DICT_SEND)
        send_msg(test_socket, DICT_SEND)
        self.assertNotIsInstance(test_socket.encoded_message, dict)

    def test_get_msg_ok(self):
        test_socket_ok = TestSocket(OK_DICT)
        self.assertEqual(get_msg(test_socket_ok), OK_DICT)

    def test_get_msg_err(self):
        test_socket_err = TestSocket(ERROR_DICT)
        self.assertEqual(get_msg(test_socket_err), ERROR_DICT)

    def test_dict_get_msg(self):
        test_socket_ok = TestSocket(OK_DICT)
        self.assertIsInstance(get_msg(test_socket_ok), dict)

    def test_no_str_get_msg(self):
        test_socket = TestSocket(DICT_SEND)
        send_msg(test_socket, DICT_SEND)
        self.assertNotIsInstance(test_socket.encoded_message, str)


if __name__ == '__main__':
    unittest.main()
