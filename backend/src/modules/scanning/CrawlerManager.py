# Crawler Manager

import os
import json
import asyncio
import requests
from collections import defaultdict
from crawler_rp import ResponseProcessor  # Make sure filename matches
from mock_http_client import MockHTTPClient  # <-- Importing our mock client

class CrawlerManager:
    def __init__(self):
        self.results = defaultdict(list)
        self.config = {}
        self.crawl_tree = {}

    def configure_crawler(self, target_url: str, depth: int, limit: int, user_agent: str, delay: int, proxy: str) -> None:
        self.config = {
            "target_url": target_url,
            "depth": depth,
            "limit": limit,
            "user_agent": user_agent,
            "delay": delay,
            "proxy": proxy
        }
        print(f"Crawler configured with target: {target_url}, depth: {depth}, limit: {limit}, delay: {delay}s")

    async def start_crawl(self) -> None:
        if not self.config:
            raise ValueError("Crawler not configured")

        # Simulate fetching HTML using mock class
        raw_html = MockHTTPClient.fetch_html(self.config["target_url"])

        # Pass raw HTML into ResponseProcessor
        rp = ResponseProcessor(self.config["target_url"])
        await rp.run(raw_html=raw_html, depth=self.config["depth"])
        rp.export_tree("site_structure_output.txt")

        # For demo, storing extracted URLs as results
        processed_data = {
            "extracted_urls": rp.extracted_urls,
            "base_url": self.config["target_url"]
        }
        self.process_response(processed_data)

    def process_response(self, response: dict) -> None:
        if not isinstance(response, dict):
            raise ValueError("Response not a dictionary")
        self.results["processed_response"].append(response)

    def store_results(self, fastapi_url: str) -> None:
        try:
            response = requests.post(fastapi_url, json=dict(self.results), headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                print("Results sent to FastAPI")
            else:
                print(f"Failed sending results - Status: {response.status_code}")
        except Exception as e:
            print(f"Error sending results: {e}")

    def reset_crawler(self) -> None:
        self.results.clear()
        self.config.clear()
        self.crawl_tree.clear()

    def display_results(self) -> None:
        print("Displaying crawl results:")
        print(json.dumps(self.results, indent=4))

    def get_crawl_tree(self) -> dict:
        return self.crawl_tree


# --- Run Block ---
if __name__ == "__main__":
    crawler_manager = CrawlerManager()
    crawler_manager.configure_crawler(
        target_url="https://crawler.com",
        depth=2,
        limit=100,
        user_agent="Mozilla/5.0",
        delay=1,
        proxy=""
    )
    asyncio.run(crawler_manager.start_crawl())
    crawler_manager.store_results("http://crawlerapi.com")
    crawler_manager.reset_crawler()