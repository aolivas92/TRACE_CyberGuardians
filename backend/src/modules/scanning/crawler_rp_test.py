import unittest
import asyncio
from crawler_rp import ResponseProcessor
from mock_http_client import MockHTTPClient

class ResponseProcessorTest(unittest.IsolatedAsyncioTestCase):
    async def test_run_and_export_with_mock_html(self):
        html = MockHTTPClient.fetch_html("https://testsite.com")
        processor = ResponseProcessor("https://testsite.com")
        await processor.run(html)

        expected_urls = ['/nav/page1.html', '/nav/page2.html', '/nav/page3.html', '/nav/page4.html', '/nav/page5.html', '/pages/page1.html', '/pages/page2.html', '/pages/page3.html', '/pages/page4.html', '/pages/page5.html', 'https://example.com', 'https://example.org', 'https://test.example.net/path?param=value', '#section', 'mailto:test@example.com', '/images/image1.jpg', '/images/image2.jpg', '/images/image3.jpg', '/submit/form1', '/sitemap.html', '/contact.html', 'styles.css', 'script.js']
        for url in expected_urls:
            self.assertIn(url, processor.extracted_urls)

        self.assertEqual(len(processor.extracted_urls), len(expected_urls))
        processor.export_tree("test_output.txt")

    def test_invalid_process_input(self):
        processor = ResponseProcessor("https://testsite.com")
        with self.assertRaises(ValueError):
            processor.process(123)

if __name__ == "__main__":
    unittest.main()