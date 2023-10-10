import parser
import unittest
from unittest.mock import patch, Mock

class TestParser(unittest.TestCase):
    @patch.object(parser, 'parse_json')
    def test_parse(self, mock_parse):
        mock_parse.return_value = True
        json_str = '''
        {
            "key1": "word1 word2",
            "key2": "word2 word3"
        }
        '''
        result = parser.parse_json(json_str, parser.callback)

        mock_parse.assert_called()