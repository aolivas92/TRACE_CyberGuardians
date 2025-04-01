# crawler_manager.py
import asyncio
import datetime
import json
from urllib.parse import urljoin
from crawler_response import CrawlerResponseProcessor
from mock_http import RealHTTPClient
from bs4 import BeautifulSoup

class CrawlerManager:
    def __init__(self):
        self.config = {}
        self.http_client = RealHTTPClient()
        self.processor = CrawlerResponseProcessor()
        self.visited = set()
        self.results = []
        self.table_data = []
        self.counter = 1

    def configure_crawler(self, target_url: str, depth: int, limit: int, user_agent: str, delay: int, proxy: str, crawl_date: str = None, crawl_time: str = None, excluded_urls: str = None):
        self.config = {
            "target_url": target_url,
            "depth": depth,
            "limit": limit,
            "user_agent": user_agent,
            "delay": delay,
            "proxy": proxy,
            "crawl_date": crawl_date,
            "crawl_time": crawl_time,
            "excluded_urls": excluded_urls.split(',') if excluded_urls else []
        }

    async def crawl_recursive(self, url, depth_remaining):
        if url in self.visited or depth_remaining < 0 or len(self.visited) >= self.config.get("limit", 100):
            return

        self.visited.add(url)
        headers = {"User-Agent": self.config.get("user_agent", "")}

        try:
            raw_html = await self.http_client.get(url, headers=headers, proxy=self.config.get("proxy"))
            await asyncio.sleep(self.config.get("delay", 0) / 1000.0)

            if depth_remaining == self.config.get("depth"):
                with open("raw_html.txt", "w", encoding="utf-8") as f:
                    f.write(raw_html)

            soup = BeautifulSoup(raw_html, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"
            text = soup.get_text()
            word_count = len(text.split())
            char_count = len(text)
            links_found = len(soup.find_all("a"))

            self.table_data.append({ "id": self.counter, "url": url, "title": title, "wordCount": word_count, "charCount": char_count, "linksFound": links_found, "error": False})
            self.counter += 1

            processed_result = self.processor.process_response(raw_html, base_url=url)
            self.results.append({"url": url, "data": processed_result})

            for extracted_url in processed_result.get("extracted_urls", []):
                if any(excluded in extracted_url for excluded in self.config["excluded_urls"]):
                    continue
                full_url = urljoin(url, extracted_url)
                await self.crawl_recursive(full_url, depth_remaining - 1)

        except Exception as e:
            self.table_data.append({
                "id": self.counter,
                "url": url,
                "title": "Error",
                "wordCount": 0,
                "charCount": 0,
                "linksFound": 0,
                "error": True
            })
            self.counter += 1

    async def start_crawl(self):
        await self.crawl_recursive(self.config.get("target_url"), self.config.get("depth"))

        with open("crawler_table_data.json", "w", encoding="utf-8") as f:
            json.dump(self.table_data, f, indent=1)

        print("Crawling completed. Results written to crawler_table_data.json")
        return self.results

if __name__ == "__main__":
    manager = CrawlerManager()
    manager.configure_crawler(
        target_url="http://localhost:5000",
        depth=5,
        limit=100,
        user_agent="Mozilla/5.0",
        delay=1000,
        proxy="8080",
        crawl_date=str(datetime.date.today()),
        crawl_time="22:00",
        excluded_urls="/login,/admin"
    )

    try:
        loop = asyncio.get_running_loop()
        task = loop.create_task(manager.start_crawl())
        loop.run_until_complete(task)
    except RuntimeError:
        asyncio.run(manager.start_crawl())
