import unittest
from unittest.mock import Mock
from crawler_process_response import CrawlerResponseProcessor

class TestCrawlerResponseProcessor(unittest.TestCase):

    def setUp(self):
        # Mock all dependencies
        self.logger_mock = Mock()
        self.parser_mock = Mock()
        self.cleaner_mock = Mock()
        self.validator_mock = Mock()
        self.http_client_mock = Mock()

        self.processor = CrawlerResponseProcessor(
            logger=lambda: self.logger_mock,
            parser=lambda: self.parser_mock,
            cleaner=lambda: self.cleaner_mock,
            validator=lambda: self.validator_mock
        )

    def test_process_response_successful(self):
        raw_content = "<html><a href='http://example.com'>Link</a></html>"
        parsed_data = {'urls': ['http://example.com']}
        cleaned_data = {'urls': ['http://example.com'], 'cleaned': True}

        self.parser_mock.parse.return_value = parsed_data
        self.cleaner_mock.clean.return_value = cleaned_data
        self.validator_mock.is_valid.return_value = True

        result = self.processor.process_response(raw_content)
        self.assertEqual(result, cleaned_data)
        self.logger_mock.info.assert_any_call("Processing raw crawler response.")
        self.logger_mock.info.assert_any_call("Processed response successfully.")

    def test_process_response_invalid(self):
        raw_content = ""
        with self.assertRaises(ValueError):
            self.processor.process_response(raw_content)
        self.logger_mock.error.assert_called_once_with("InvalidResponse: raw_content is empty.")


    def test_send_filtered_urls_valid_urls(self):
        cleaned_data = {'urls': ['http://valid-url.com']}
        self.http_client_mock.send.return_value = None

        self.processor.send_filtered_urls(cleaned_data, self.http_client_mock)
        self.logger_mock.info.assert_any_call("Sending 1 filtered URLs to HTTP client.")
        self.logger_mock.debug.assert_any_call("Updated HTTP client's request queue.")
        self.http_client_mock.send.assert_called_once_with('http://valid-url.com')

    def test_send_filtered_urls_no_valid_urls(self):
        cleaned_data = {'urls': []}
        self.processor.send_filtered_urls(cleaned_data, self.http_client_mock)
        self.logger_mock.warning.assert_called_once_with("No valid URLs to send.")

if __name__ == "__main__":
    unittest.main()
