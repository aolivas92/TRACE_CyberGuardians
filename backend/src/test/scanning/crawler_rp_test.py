import unittest
import asyncio
from src.modules.scanning.crawler_rp import ResponseProcessor
from src.modules.scanning.mock_http_client import MockHTTPClient

class ResponseProcessorTest(unittest.IsolatedAsyncioTestCase):
    async def test_recursive_run_and_crawl_tree(self):
        html = MockHTTPClient.fetch_html("https://testsite.com")
        processor = ResponseProcessor("https://testsite.com")
        await processor.run(html, depth=1)

        # Ensure some URLs were discovered
        self.assertTrue(len(processor.extracted_urls) > 0)

        # Ensure crawl tree is built and includes root
        crawl_tree = processor.crawl_tree
        self.assertIn("https://testsite.com", crawl_tree)

        # Verify recursive child URLs were added
        for child in crawl_tree["https://testsite.com"]:
            self.assertTrue(child.startswith("https://testsite.com"))

        processor.export_tree("test_output.txt")

    def test_invalid_process_input(self):
        processor = ResponseProcessor("https://testsite.com")
        with self.assertRaises(ValueError):
            processor.process(123)

if __name__ == "__main__":
    unittest.main()
