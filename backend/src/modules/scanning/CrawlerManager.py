# Crawler Manager

import re
import time
import json
import asyncio
import aiohttp
import requests
from collections import deque
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urljoin, urlparse
from src.modules.scanning.crawler_rp import ResponseProcessor

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
        self.response_processor = ResponseProcessor(base_url=base_url)

    async def fetch(self, session, url):
        try:
            async with session.get(url, headers={"User-Agent": self.user_agent}, ssl=False) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            print(f"Failed fetching {url}: {e}")
        return None

    async def crawl(self):
        async with aiohttp.ClientSession() as session:
            while self.queue and len(self.visited) < self.limit:
                url, depth = self.queue.popleft()
                if url in self.visited or depth > self.depth:
                    continue
                print(f"Crawling: {url} Depth: {depth}")
                self.visited.add(url)
                html = await self.fetch(session, url)
                if not html:
                    continue
                processed_response = await self.response_processor.run(html)
                self.results[url] = processed_response
                child_links = self.extract_links(html, url)
                self.crawl_tree[url] = list(child_links)
                for link in child_links:
                    if link not in self.visited:
                        self.queue.append((link, depth + 1))
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
    
    def configure_crawler(self, target_url, depth, limit, user_agent, delay, extra):
        self.base_url = target_url
        self.depth = depth
        self.limit = limit
        self.user_agent = user_agent
        self.delay = delay
        self.config = {"target_url": target_url, "depth": depth, "limit": limit, "user_agent": user_agent, "delay": delay, "extra": extra,}
    
    async def start_crawl(self):
        await self.crawl()

    def get_crawl_results(self):
        return self.results
    
    def process_response(self, response):
        if not isinstance(response, dict):
            raise ValueError("Invalid response")
        if "processed_response" not in self.results:
            self.results["processed_response"] = []
        self.results["processed_response"].append(response)
    
    def store_results(self, api_url):
        import requests
        headers = {"Content-Type": "application/json"}
        response = requests.post(api_url, json=self.results, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed storing results: {response.status_code}")
    
    def reset_crawler(self):
        self.results = {}
        self.config = {}
        self.crawl_tree = {}


crawler = CrawlerManager(base_url="https://test.com", depth=2, limit=10, user_agent="MyCrawler", delay=1)
asyncio.run(crawler.crawl())
print(json.dumps(crawler.get_crawl_results(), indent=4))