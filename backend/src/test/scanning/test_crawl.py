#!/usr/bin/env python3
import asyncio
import os
import json
import shutil
import unittest
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

# Add the parent directory to sys.path to import the crawler modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the crawler modules
from src.modules.scanning.crawler_manager import crawler_manager
from src.modules.scanning.crawler_response import CrawlerResponseProcessor



class TestCrawlerManager(unittest.TestCase):
    def setUp(self):
        """Setup runs before each test"""
        self.manager = crawler_manager()
        self.test_config = {
            "target_url": "http://example.com",
            "depth": 2,
            "limit": 10,
            "user_agent": "TestAgent",
            "delay": 0,
            "proxy": None,
            "crawl_date": "2025-04-12",
            "crawl_time": "12:00",
            "excluded_urls": "http://exclude.com,http://test.com"
        }
    def test_crawler_states(self):
        self.manager.stop()
        self.assertTrue(self.manager._stopped)

        self.manager.pause()
        self.assertTrue(self.manager._paused)

        self.manager.resume()
        self.assertFalse(self.manager._paused)   


    def test_configure_crawler(self):
        manager = crawler_manager()
        manager.configure_crawler(
            target_url="http://example.com",
            depth=3,
            limit=10,
            user_agent="TestAgent",
            delay=500,
            proxy="http://proxy.com",
            crawl_date="2025-04-12",
            crawl_time="12:00",
            excluded_urls="http://exclude.com,http://test.com"
        )
        
        self.assertEqual(manager.config["target_url"], "http://example.com")
        self.assertEqual(manager.config["depth"], 3)
        self.assertEqual(manager.config["limit"], 10)
        self.assertEqual(manager.config["user_agent"], "TestAgent")
        self.assertEqual(manager.config["delay"], 500)
        self.assertEqual(manager.config["proxy"], "http://proxy.com")
        self.assertEqual(manager.config["crawl_date"], "2025-04-12")
        self.assertEqual(manager.config["crawl_time"], "12:00")
        self.assertEqual(manager.config["excluded_urls"], ["http://exclude.com", "http://test.com"])


    @patch("src.modules.scanning.crawler_manager.RealHTTPClient.get", new_callable=AsyncMock)
    def test_start_crawl(self, mock_http_get):
        """Test full crawl process"""
        async def run_test():
            # Setup mock
            mock_http_get.return_value = "<html><body>Test</body></html>"
            
            # Configure and start crawl
            self.manager.configure_crawler(**self.test_config)
            results = await self.manager.start_crawl()

            # Verify results
            self.assertTrue(isinstance(results, list))
            self.assertTrue(len(results) > 0)
            self.assertIn("url", results[0])
            self.assertIn("data", results[0])

        # Run the async test
        asyncio.run(run_test())
    
    @patch("src.modules.scanning.crawler_manager.RealHTTPClient.get", new_callable=AsyncMock)
    @patch("src.modules.scanning.crawler_manager.BeautifulSoup")
    def test_crawl_recursive(self, mock_soup, mock_http_get):
        """Test recursive crawling with mocked HTTP responses"""
        async def run_test():
            # Setup mocks
            html_content = "<html><body><a href='http://example.com/page1'>Link</a></body></html>"
            mock_http_get.return_value = html_content
            
            mock_soup_instance = MagicMock()
            mock_soup_instance.find_all.return_value = [{"href": "http://example.com/page1"}]
            mock_soup_instance.title.string = "Test Page"
            mock_soup_instance.get_text.return_value = "Test content"
            mock_soup.return_value = mock_soup_instance

            # Configure and start crawl
            self.manager.configure_crawler(**self.test_config)
            await self.manager.crawl_recursive("http://example.com", 2)

            # Verify results
            print(f"visited URLs: {self.manager.visited}")
            print(f"results: {self.manager.results}")
            self.assertIn("http://example.com", self.manager.visited)
            self.assertTrue(len(self.manager.results) > 0)
            self.assertEqual(self.manager.results[0]["url"], "http://example.com")

        # Run the async test
        asyncio.run(run_test())

if __name__ == "__main__":
    unittest.main()