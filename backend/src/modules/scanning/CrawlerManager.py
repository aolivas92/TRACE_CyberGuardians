# Crawler Manager

import asyncio
import datetime
from urllib.parse import urljoin
from src.modules.scanning.mock_http import RealHTTPClient
from src.modules.scanning.crawler_response import CrawlerResponseProcessor

class CrawlerManager:
    def __init__(self):
        self.config = {}
        self.results = []
        self.visited = set()
        self.http_client = RealHTTPClient()
        self.processor = CrawlerResponseProcessor()

    def configure_crawler(self, target_url: str, depth: int, limit: int, user_agent: str, delay: int, proxy: str, crawl_date: str = None, crawl_time: str = None, excluded_urls: str = None):
        self.config = {"target_url": target_url, "depth": depth, "user_agent": user_agent, "delay": delay,
            "proxy": proxy, "crawl_date": crawl_date, "crawl_time": crawl_time,
            "excluded_urls": excluded_urls.split(',') if excluded_urls else []}

    async def crawl_recursive(self, url, depth_remaining):
        if url in self.visited or depth_remaining < 0 or len(self.visited) >= self.config.get("limit", 100):
            return
        self.visited.add(url)
        headers = {"User-Agent": self.config.get("user_agent", "")}
        raw_html = await self.http_client.get(url, headers=headers, proxy=self.config.get("proxy"))
        await asyncio.sleep(self.config.get("delay", 0) / 1000.0)
        if depth_remaining == self.config.get("depth"):
            with open("raw_html.txt", "w", encoding="utf-8") as f:
                f.write(raw_html)
        processed_result = self.processor.process_response(raw_html, base_url=url)
        self.results.append({"url": url, "data": processed_result})
        for extracted_url in processed_result.get("extracted_urls", []):
            if any(excluded in extracted_url for excluded in self.config["excluded_urls"]):
                continue
            full_url = urljoin(url, extracted_url)
            await self.crawl_recursive(full_url, depth_remaining - 1)

    async def start_crawl(self):
        await self.crawl_recursive(self.config.get("target_url"), self.config.get("depth"))
        with open("crawler_results.txt", "w", encoding="utf-8") as f:
            for entry in self.results:
                f.write(str(entry) + "\n")
        print("Crawling completed")
        results_file = "crawler_results.txt"
        print(f"Results stored in {results_file}")
        return self.results

manager = CrawlerManager()
manager.configure_crawler( target_url="http://localhost:5000", depth=3, limit=100, user_agent="Mozilla/5.0",
    delay=1000, proxy="8080", crawl_date=str(datetime.date.today()), crawl_time="22:00", excluded_urls="/login,/admin")
try:
    loop = asyncio.get_running_loop()
    task = loop.create_task(manager.start_crawl())
    loop.run_until_complete(task)
except RuntimeError:
    asyncio.run(manager.start_crawl())