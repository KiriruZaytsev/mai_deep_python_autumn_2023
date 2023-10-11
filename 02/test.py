import jsonparser as jp
import unittest
from unittest.mock import patch, Mock
from time import sleep, time


class TestParser(unittest.TestCase):

    json_str = '{"field1": "value1 value2", "field2": "value3 value4"}'

    def test_timer(self):
        with jp.timer() as exec_time:
            sleep(1)
        curr_time = exec_time()
        self.assertTrue(curr_time >= 1.0)

        with jp.timer() as exec_time:
            pass
        curr_time = exec_time()
        self.assertTrue(curr_time <= 0.1)
    
    def test_parser_with_no_callback(self):
        wrong_callback = None
        self.assertRaises(TypeError, jp.parse_json, self.json_str, wrong_callback)

    def test_parser_with_invalid_str(self):
        callback_mock = Mock()
        error_json = 'invalid_name'
        with self.assertRaises(ValueError):
            jp.parse_json(error_json, callback_mock)
        callback_mock.assert_not_called()

    def test_parser_with_default_args(self):
        callback_mock = Mock()
        jp.parse_json(self.json_str, callback_mock)
        self.assertTrue(callback_mock.called)
        self.assertEqual(callback_mock.call_count, 4)

    def test_parser_without_keywords(self):
        callback_mock = Mock()
        jp.parse_json(self.json_str, callback_mock, ['field1'])
        self.assertTrue(callback_mock.called)
        self.assertEqual(callback_mock.call_count, 2)

    def test_parser_without_field(self):
        callback_mock = Mock()
        jp.parse_json(self.json_str, callback_mock, keywords=['value1', 'value2', 'value3'])
        self.assertTrue(callback_mock.called)
        self.assertEqual(callback_mock.call_count, 3)

    def test_parser_with_fields_and_keywords(self):
        callback_mock = Mock()
        jp.parse_json(self.json_str, callback_mock, ['field1'], ['value1'])
        self.assertTrue(callback_mock.called)
        self.assertEqual(callback_mock.call_count, 1)

    def test_default_callback(self):
        with jp.timer() as exec_time:
            jp.callback('field1', 'value1')
        curr_time = exec_time()
        self.assertTrue(curr_time <= 2)
        