# Crawler Manager Test

import asyncio
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from src.modules.scanning.CrawlerManager import CrawlerManager

class CrawlerManagerTest(unittest.TestCase):
    #@patch("CrawlerManager.ResponseProcessor")
    @patch("src.modules.scanning.CrawlerManager.requests.post")
    @patch("src.modules.scanning.CrawlerManager.aiohttp.ClientSession.get")
    @patch("src.modules.scanning.CrawlerManager.aiohttp.ClientSession")
    def setUp(self, MockClientSession, mock_get, MockResponseProcessor):
        self.mock_response_processor = MagicMock()
        MockResponseProcessor.return_value = self.mock_response_processor
        self.mock_response_processor.run.return_value = {"processed": "data"}
        self.mock_response = MagicMock()
        self.mock_response.status = 200
        #self.mock_response.text.return_value = asyncio.Future()
        #self.mock_response.text.return_value.set_result("<html></html>")
        self.mock_response.text = AsyncMock(return_value="<html></html>")
        mock_get.return_value = self.mock_response
        self.mock_session = AsyncMock()
        MockClientSession.return_value = self.mock_session
        self.mock_session.__aenter__.return_value = self.mock_session
        self.crawler = CrawlerManager(base_url="https://test.com", depth=2, limit=10, user_agent="TestAgent", delay=1)

    #@patch("CrawlerManager.requests.post")
    @patch("src.modules.scanning.CrawlerManager.requests.post")
    def test_store_results(self, mock_post):
        mock_post.return_value.status_code = 200
        self.crawler.results = {"processed_response": [{"key": "value"}]}
        self.crawler.store_results("https://api.store.com")
        mock_post.assert_called_once_with("https://api.store.com", json=self.crawler.results, headers={"Content-Type": "application/json"})

    #@patch("CrawlerManager.requests.post")
    @patch("src.modules.scanning.CrawlerManager.requests.post")
    def test_store_results_failure(self, mock_post):
        mock_post.return_value.status_code = 500
        self.crawler.results = {"processed_response": [{"key": "value"}]}
        with self.assertRaises(Exception):
            self.crawler.store_results("https://api.store.com")

    def test_reset_crawler(self):
        self.crawler.results = {"processed_response": [{"key": "value"}]}
        self.crawler.config = {"key": "config_value"}
        self.crawler.crawl_tree = {"https://test.com": ["https://child.com"]}
        self.crawler.reset_crawler()
        self.assertEqual(self.crawler.results, {})
        self.assertEqual(self.crawler.config, {})
        self.assertEqual(self.crawler.crawl_tree, {})

unittest.main()