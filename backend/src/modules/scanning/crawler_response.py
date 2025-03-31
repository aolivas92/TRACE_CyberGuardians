# crawler_response_processor.py
import asyncio
from bs4 import BeautifulSoup

class MockHTTPClient:
    async def get(self, url, headers=None, proxy=None):
        await asyncio.sleep(0.1)
        return self.get_test_html()

    def get_test_html(self):
        with open("raw_html.txt", "r", encoding="utf-8") as f:
            return f.read()

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.children = []

class BST:
    def __init__(self):
        self.root = None
        self.node_map = {}

    def insert(self, parent, value):
        if value in self.node_map:
            return self.node_map[value]
        new_node = Node(value)
        self.node_map[value] = new_node
        if parent:
            parent.children.append(new_node)
        if not self.root:
            self.root = new_node
        return new_node

    def build_tree(self, root_url, children):
        root_node = self.insert(None, root_url)
        for url in children:
            self.insert(root_node, url)

    def _write_tree(self, node, depth, lines):
        if node:
            lines.append("  " * depth + node.value)
            for child in node.children:
                self._write_tree(child, depth + 1, lines)

    def save_tree_to_file(self, filename):
        lines = []
        self._write_tree(self.root, 0, lines)
        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")

class CrawlerResponseProcessor:
    def __init__(self):
        self.bst = BST()

    def process_response(self, raw_html: str, base_url: str = "") -> dict:
        soup = BeautifulSoup(raw_html, "html.parser")
        urls = set()

        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if not href.startswith("mailto:") and not href.startswith("#"):
                urls.add(href)
        for tag in soup.find_all("link", href=True):
            urls.add(tag["href"])
        for tag in soup.find_all("script", src=True):
            urls.add(tag["src"])
        for tag in soup.find_all("img", src=True):
            urls.add(tag["src"])
        for tag in soup.find_all("form", action=True):
            urls.add(tag["action"])

        # Insert all URLs as children of base_url in the tree
        self.bst.build_tree(base_url, urls)
        self.bst.save_tree_to_file("extracted_urls_tree.txt")

        return {
            "processor": "CrawlerResponseProcessor",
            "extracted_urls": sorted(list(urls)),
            "count": len(urls),
            "exmaple.com": ["exmpale.com/nav", "exmpale.com/nav/pag1"]
        }
