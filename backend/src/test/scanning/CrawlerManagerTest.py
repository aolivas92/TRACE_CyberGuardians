# Crawler Manager Test

import unittest
from unittest.mock import AsyncMock, MagicMock
from CrawlerManager import CrawlerManager

class TestCrawlerManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.base_url = "http://crawler.com"
        self.depth = 2
        self.limit = 5
        self.user_agent = "TestBot"
        self.delay = 0
        self.crawler = CrawlerManager(self.base_url, self.depth, self.limit, self.user_agent, self.delay)

    async def test_crawl_single_page(self):
        mock_html_provider = AsyncMock(return_value="<html><body><a href='/page1'>Page 1</a></body></html>")
        await self.crawler.start_crawl(mock_html_provider)
        self.assertIn(self.base_url, self.crawler.visited)
        self.assertIn("http://crawler.com/page1", self.crawler.crawl_tree[self.base_url])

    async def test_crawl_respects_limit(self):
        mock_html_provider = AsyncMock(side_effect=["<html><body><a href='/page1'>Page 1</a><a href='/page2'>Page 2</a></body></html>",
        "<html><body><a href='/page3'>Page 3</a></body></html>",
        "<html><body><a href='/page4'>Page 4</a></body></html>",
        "<html><body><a href='/page5'>Page 5</a></body></html>", ""]) 
        await self.crawler.start_crawl(mock_html_provider)
        self.assertLessEqual(len(self.crawler.visited), self.limit)

    async def test_crawl_ignores_visited_pages(self):
        mock_html_provider = AsyncMock(return_value="<html><body><a href='/page1'>Page 1</a></body></html>")
        await self.crawler.start_crawl(mock_html_provider)
        await self.crawler.start_crawl(mock_html_provider)
        self.assertEqual(len(self.crawler.visited), 2)

    async def test_crawl_handles_empty_html(self):
        mock_html_provider = AsyncMock(return_value="")
        await self.crawler.start_crawl(mock_html_provider)
        self.assertEqual(len(self.crawler.visited), 1)

    async def test_reset_crawler(self):
        self.crawler.visited.add(self.base_url)
        self.crawler.results[self.base_url] = "Test Result"
        self.crawler.crawl_tree[self.base_url] = ["http://crawler.com/page1"]
        self.crawler.reset_crawler()
        self.assertEqual(len(self.crawler.visited), 0)
        self.assertEqual(self.crawler.results, {})
        self.assertEqual(self.crawler.crawl_tree, {})

unittest.main()