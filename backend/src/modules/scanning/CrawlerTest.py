import time
import random
import unittest
from requests.models import Response
from mockito import mock, when, verify, at_least
from CrawlerManager import CrawlerManager, CrawlerResponseProcessor, Logger, Parser, Cleaner, Validator

class TestCrawlerManager(unittest.TestCase):
    def test_start_crawl(self):
        crawler_manager = CrawlerManager()
        crawler_manager.configure_crawler(target_url="http://crawler.com", depth=2, limit=100, user_agent="Mozilla/5.0", delay=1, proxy="")
        when(random).choice().thenReturn("/home")
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
        verify(requests, at_least(1)).post("http://crawlerapi.com", json=crawler_manager.results)

class TestCrawlerResponseProcessor(unittest.TestCase):    
    def test_process_response(self):
        logger = mock(Logger)
        parser = mock(Parser)
        cleaner = mock(Cleaner)
        validator = mock(Validator)
        raw_content = "Here are some URLs: http://crawler1.com http://crawler2.com"
        when(parser).parse(raw_content).thenReturn({"urls": ["http://crawler1.com", "http://crawler2.com"]})
        when(cleaner).clean({"urls": ["http://crawler1.com", "http://crawler2.com"]}).thenReturn({"urls": ["http://crawler1.com", "http://crawler2.com"], "cleaned": True})
        when(validator).is_valid({"urls": ["http://crawler1.com", "http://crawler2.com"], "cleaned": True}).thenReturn(True)
        response_processor = CrawlerResponseProcessor(logger, parser, cleaner, validator)
        processed_data = response_processor.process_response(raw_content)
        self.assertEqual(processed_data, {"urls": ["http://crawler1.com", "http://crawler2.com"], "cleaned": True})
        verify(parser).parse(raw_content)
        verify(cleaner).clean({"urls": ["http://crawler1.com", "http://crawler2.com"]})
        verify(validator).is_valid({"urls": ["http://crawler1.com", "http://crawler2.com"], "cleaned": True})

unittest.main()