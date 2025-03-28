# Crawler Manager Test

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from src.modules.scanning.CrawlerManager import CrawlerManager

class CrawlerManagerTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.CrawlerManager = CrawlerManager(base_url="https://test.com", depth=2, limit=10, user_agent="TestAgent", delay=0)

    def test_configure_crawler(self):
        self.CrawlerManager.configure_crawler("https://Crawler.com", 2, 100, "TestAgent", 1, "")
        self.assertEqual(self.CrawlerManager.config["target_url"], "https://Crawler.com")
        self.assertEqual(self.CrawlerManager.config["depth"], 2)
    
    """

    @patch("src.modules.scanning.CrawlerManager.ResponseProcessor")
    async def test_start_crawl(self, mock_response_processor):
        mock_rp_instance = mock_response_processor.return_value
        mock_rp_instance.run = AsyncMock()
        mock_rp_instance.export_tree = MagicMock()
        mock_rp_instance.tree = {}
        mock_rp_instance.external_links = []
        self.CrawlerManager.configure_crawler("https://Crawler.com", 2, 100, "TestAgent", 1, "")
        await self.CrawlerManager.start_crawl()
        mock_rp_instance.run.assert_called()
        mock_rp_instance.export_tree.assert_called()
        """
    @patch.object(CrawlerManager, 'fetch', new_callable=AsyncMock)
    async def test_start_crawl(self, mock_fetch):
        mock_fetch.return_value = "<html><a href='/next'></a></html>"
        await self.CrawlerManager.start_crawl()
        self.assertIn("https://test.com", self.CrawlerManager.crawl_tree)

    def test_process_response_valid(self):
        response = {"key": "value"}
        self.CrawlerManager.process_response(response)
        self.assertIn("processed_response", self.CrawlerManager.results)
        self.assertEqual(self.CrawlerManager.results["processed_response"], [response])

    def test_process_response_invalid(self):
        with self.assertRaises(ValueError):
            self.CrawlerManager.process_response([])

    @patch("src.modules.scanning.CrawlerManager.requests.post")
    def test_store_results(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        self.CrawlerManager.results = {"processed_response": [{"key": "value"}]}
        self.CrawlerManager.store_results("http://api.Crawler.com")
        mock_post.assert_called_once_with("http://api.Crawler.com", json={"processed_response": [{"key": "value"}]}, headers={"Content-Type": "application/json"},)

    def test_reset_crawler(self):
        self.CrawlerManager.results = {"key": "value"}
        self.CrawlerManager.config = {"key": "value"}
        self.CrawlerManager.crawl_tree = {"key": "value"}
        self.CrawlerManager.reset_crawler()
        self.assertEqual(self.CrawlerManager.results, {})
        self.assertEqual(self.CrawlerManager.config, {})
        self.assertEqual(self.CrawlerManager.crawl_tree, {})

unittest.main()