import time
import random
import unittest
from requests.models import Response
import requests
from mockito import mock, when, verify
from CrawlerManager import CrawlerManager, CrawlerResponseProcessor, Logger, Parser, Cleaner, Validator

class TestCrawlerManager(unittest.TestCase):
    def test_start_crawl(self):
        crawler_manager = CrawlerManager()
        crawler_manager.configure_crawler(target_url="http://crawler.com", depth=2, limit=100, user_agent="Mozilla/5.0", delay=1, proxy="")
        when(random).choice(["/", "/home", "/var", "/usr", "/etc"]).thenReturn("/home")
        when(time).sleep(2).thenReturn(None)
        crawler_manager.start_crawl()
        self.assertIn("directories", crawler_manager.results)
        self.assertIn("connections", crawler_manager.results)
        
    def test_process_response(self):
        crawler_manager = CrawlerManager()
        test_response = {"url": "http://crawler.com"}
        crawler_manager.process_response(test_response)
        self.assertEqual(crawler_manager.results["processed_response"], test_response)
        
    def test_save_results(self):
        crawler_manager = CrawlerManager()
        crawler_manager.results = {"directories": ["/home", "/var"], "connections": [("a", "b"), ("c", "d")]}
        mocked_response = mock(Response)
        mocked_response.status_code = 200
        when(requests).post("http://crawlerapi.com", json=crawler_manager.results).thenReturn(mocked_response)
        crawler_manager.save_results("http://crawlerapi.com")
        verify(requests).post("http://crawlerapi.com", json=crawler_manager.results)


class TestCrawlerResponseProcessor(unittest.TestCase):
    def test_process_response(self):
        mock_logger = mock(Logger)
        mock_parser = mock(Parser)
        mock_cleaner = mock(Cleaner)
        mock_validator = mock(Validator)
        
        raw_content = "Here are some URLs: http://crawler1.com http://crawler2.com"
        when(mock_logger).info("Processing raw crawler response.").thenReturn(None)
        when(mock_logger).debug("Analyzing raw HTML for useful data.").thenReturn(None)
        when(mock_logger).debug("Normalizing and cleaning parsed data.").thenReturn(None)
        when(mock_logger).debug("Validating the cleaned data.").thenReturn(None)
        when(mock_logger).info("Processed response successfully.").thenReturn(None)
        
        when(mock_parser).parse(raw_content).thenReturn({"urls": ["http://crawler1.com", "http://crawler2.com"]})
        when(mock_cleaner).clean({"urls": ["http://crawler1.com", "http://crawler2.com"]}).thenReturn({"urls": ["http://crawler1.com", "http://crawler2.com"], "cleaned": True})
        when(mock_validator).is_valid({"urls": ["http://crawler1.com", "http://crawler2.com"], "cleaned": True}).thenReturn(True)
        response_processor = CrawlerResponseProcessor(mock_logger, mock_parser, mock_cleaner, mock_validator)
        processed_data = response_processor.process_response(raw_content)
        self.assertEqual(processed_data, {"urls": ["http://crawler1.com", "http://crawler2.com"], "cleaned": True})
        verify(mock_parser).parse(raw_content)
        verify(mock_cleaner).clean({"urls": ["http://crawler1.com", "http://crawler2.com"]})
        verify(mock_validator).is_valid({"urls": ["http://crawler1.com", "http://crawler2.com"], "cleaned": True})
        verify(mock_logger).info("Processing raw crawler response.")
        verify(mock_logger).debug("Analyzing raw HTML for useful data.")
        verify(mock_logger).debug("Normalizing and cleaning parsed data.")
        verify(mock_logger).debug("Validating the cleaned data.")
        verify(mock_logger).info("Processed response successfully.")

unittest.main()
