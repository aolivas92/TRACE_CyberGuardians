# fuzzer_response_processor_test.py

import unittest
from src.modules.fuzzer.fuzzer_response_processor import FuzzerResponseProcessor

class MockResponse:
    def __init__(self, url, status_code, text, payload=None, error=False):
        self.url = url
        self.status_code = status_code
        self.text = text
        self.payload = payload
        self.error = error

class TestFuzzerResponseProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = FuzzerResponseProcessor()

    def test_set_filters(self):
        self.processor.set_filters(status_filter=[200, 500], hide_codes=[403], length_threshold=50)
        self.assertEqual(self.processor.status_code_filter, [200, 500])
        self.assertEqual(self.processor.hide_codes, [403])
        self.assertEqual(self.processor.length_threshold, 50)

    def test_process_response_valid(self):
        self.processor.set_filters(status_filter=[200], hide_codes=[], length_threshold=10)
        response = MockResponse(
            url="http://test.com",
            status_code=200,
            text="This is a valid response body exceeding the length threshold.",
            payload="injected-payload"
        )
        self.processor.process_response(response)
        results = self.processor.get_filtered_results()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], 200)
        self.assertEqual(results[0]["url"], "http://test.com")
        self.assertEqual(results[0]["payload"], "injected-payload")
        self.assertIn("snippet", results[0])
        self.assertFalse(results[0]["error"])

    def test_process_response_filtered_by_hide_code(self):
        self.processor.set_filters(status_filter=[200, 403], hide_codes=[403], length_threshold=0)
        response = MockResponse(
            url="http://test.com/403",
            status_code=403,
            text="Forbidden content"
        )
        self.processor.process_response(response)
        results = self.processor.get_filtered_results()
        self.assertEqual(len(results), 0)

    def test_process_response_filtered_by_length(self):
        self.processor.set_filters(status_filter=[200], hide_codes=[], length_threshold=100)
        response = MockResponse(
            url="http://test.com/short",
            status_code=200,
            text="Too short"
        )
        self.processor.process_response(response)
        results = self.processor.get_filtered_results()
        self.assertEqual(len(results), 0)

unittest.main()