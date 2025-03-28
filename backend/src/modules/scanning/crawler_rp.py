import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Dict, List, Union
import asyncio

class ResponseProcessor:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.extracted_urls: List[str] = []
        self.domain_structure: Dict[str, List[str]] = {}
        self.raw_html_store_path = "raw_html.txt"

    async def run(self, raw_html: str, depth: int = 0) -> None:
        from src.modules.scanning.mock_http_client import MockHTTPClient
        visited = set()
        queue = [(self.base_url, raw_html, 0)]
        tree = {}

        while queue:
            current_url, current_html, current_depth = queue.pop(0)
            if current_url in visited or current_depth > depth:
                continue
            visited.add(current_url)

            self.save_raw_html(current_html)
            soup = BeautifulSoup(current_html, 'html.parser')
            self._extract_links(soup)
            tree[current_url] = []

            for link in self.extracted_urls:
                if link.startswith('/'):
                    full_url = f"{self.base_url.rstrip('/')}{link}"
                elif link.startswith(self.base_url):
                    full_url = link
                else:
                    continue  # skip external links

                if full_url not in visited:
                    linked_html = MockHTTPClient.fetch_html(full_url)
                    queue.append((full_url, linked_html, current_depth + 1))
                    tree[current_url].append(full_url)

        self.crawl_tree = tree
        """Main async method to process raw HTML input."""
        self.save_raw_html(raw_html)
        self.process(raw_html, depth)

    def save_raw_html(self, html: str) -> None:
        with open(self.raw_html_store_path, "w", encoding="utf-8") as f:
            f.write(html)

    def process(self, data: Union[str, dict, list], depth: int = 0) -> None:
        if isinstance(data, dict) or isinstance(data, list):
            text = json.dumps(data)
        elif isinstance(data, str):
            text = data
        else:
            raise ValueError("Unsupported data type. Please provide JSON or raw HTML.")

        soup = BeautifulSoup(text, 'html.parser')
        self._extract_links(soup)

    def _extract_links(self, soup: BeautifulSoup) -> None:
        tags_attrs = [
            ('a', 'href'), ('link', 'href'), ('img', 'src'),
            ('script', 'src'), ('form', 'action')
        ]

        for tag, attr in tags_attrs:
            for match in soup.find_all(tag):
                value = match.get(attr)
                if value:
                    self.extracted_urls.append(value)

    def export_tree(self, output_file: str = "site_structure.txt") -> None:
        data = {
            "processor": "CrawlerResponseProcessor",
            "extracted_urls": self.extracted_urls,
            "count": len(self.extracted_urls),
            self.base_domain: self._generate_sample_domain_structure()
        }
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _generate_sample_domain_structure(self) -> List[str]:
        example_paths = []
        for url in self.extracted_urls:
            if url.startswith("/"):
                example_paths.append(f"{self.base_domain}{url}")
        return example_paths