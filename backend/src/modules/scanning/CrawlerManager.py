# Crawler Manager

import re
import json
import time
import asyncio
from collections import deque
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from crawler_rp_parallel import ResponseProcessor

class CrawlerManager:
    def __init__(self, base_url, depth, limit, user_agent, delay):
        self.base_url = base_url
        self.depth = depth
        self.limit = limit
        self.user_agent = user_agent
        self.delay = delay
        self.visited = set()
        self.crawl_tree = {}
        self.queue = deque([(base_url, 0)])
        self.results = {}
        self.config = {}
        self.response_processor = ResponseProcessor(base_url=self.base_url)

    async def crawl(self, html_provider):
        while self.queue and len(self.visited) < self.limit:
            url, current_depth = self.queue.popleft()
            if url in self.visited or current_depth > self.depth:
                continue
            print(f"Crawling: {url} - Depth: {current_depth}")
            self.visited.add(url)
            html = await html_provider(url)
            if not html:
                continue
            print(f"Running response processor with depth: {self.depth}")
            processed_response = await self.response_processor.run(depth=self.depth, html_content=html)
            self.results[url] = processed_response
            child_links = self.extract_links(html, url)
            self.crawl_tree[url] = list(child_links)
            for link in child_links:
                if link not in self.visited and len(self.visited) < self.limit:
                    self.queue.append((link, current_depth + 1))
            await asyncio.sleep(self.delay)

    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, "html.parser")
        links = set()
        for link_tag in soup.find_all("a", href=True):
            link = link_tag["href"]
            full_url = urljoin(base_url, link)
            parsed_url = urlparse(full_url)
            if parsed_url.scheme in ["http", "https"]:
                links.add(full_url)
        return links

    async def start_crawl(self, html_provider):
        await self.crawl(html_provider)

    def get_crawl_results(self):
        return self.results

    def reset_crawler(self):
        self.results = {}
        self.config = {}
        self.crawl_tree = {}
        self.visited.clear()

async def fake_provider(url):
    return "<html><body><a href='/page1'>Page 1</a></body></html>"
async def test():
    crawler = CrawlerManager("http://crawler.com", 2, 5, "TestBot", 0)
    await crawler.start_crawl(fake_provider)
    print("Visited:", crawler.visited)
asyncio.run(test())