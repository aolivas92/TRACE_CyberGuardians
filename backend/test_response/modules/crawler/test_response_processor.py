# test_response_processor.py
import unittest
from unittest.mock import Mock
from modules.crawler.response_processor import CrawlerResponseProcessor

class TestCrawlerResponseProcessor(unittest.TestCase):

    def setUp(self):
        self.logger = Mock()
        self.parser = Mock()
        self.cleaner = Mock()
        self.validator = Mock()
        self.processor = CrawlerResponseProcessor(self.logger, self.parser, self.cleaner, self.validator)

    def test_process_json_response(self):
        response = Mock()
        response.headers = {"Content-Type": "application/json"}
        response.json.return_value = {"key": "value"}

        self.parser.parse.return_value = {"parsed": "data"}
        self.cleaner.clean.return_value = {"parsed": "data", "cleaned": True}
        self.validator.is_valid.return_value = True

        result = self.processor.process_response(response)
        self.assertTrue(result)
        self.logger.info.assert_called_with("Successfully processed response")

    def test_process_invalid_data(self):
        response = Mock()
        response.headers = {"Content-Type": "application/json"}
        response.json.return_value = {"key": "value"}

        self.parser.parse.return_value = {}
        self.cleaner.clean.return_value = {}
        self.validator.is_valid.return_value = False

        result = self.processor.process_response(response)
        self.assertIsNone(result)
        self.logger.warning.assert_called_with("Data validation failed.")

    def test_process_error_handling(self):
        response = Mock()
        response.headers = {"Content-Type": "application/json"}
        response.json.side_effect = Exception("Failed to decode JSON")

        result = self.processor.process_response(response)
        self.assertIsNone(result)
        self.logger.error.assert_called()

if __name__ == "__main__":
    unittest.main()