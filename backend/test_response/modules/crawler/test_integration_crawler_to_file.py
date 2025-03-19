import unittest
import os
from unittest.mock import patch, Mock
from modules.crawler import Crawler, CrawlerResponseProcessor, DummyLogger, DummyParser, DummyCleaner, DummyValidator

class IntegrationTestCrawlerProcessor(unittest.TestCase):

    def setUp(self):
        # Setup real dummy dependencies
        self.logger = DummyLogger()
        self.parser = DummyParser()
        self.cleaner = DummyCleaner()
        self.validator = DummyValidator()
        self.processor = CrawlerResponseProcessor(self.logger, self.parser, self.cleaner, self.validator)
        self.crawler = Crawler(self.processor, self.logger)
        self.output_file = os.path.join(os.path.dirname(__file__), "output_urls.txt")

    @patch('modules.crawler.crawler.requests.get')
    def test_crawler_to_url_file_output(self, mock_get):
        # Mock HTTP response with HTML containing URLs
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "text/html"}
        mock_response.text = '''
            <html>
                <body>
                    <a href="https://example.com/page1">Page 1</a>
                    <a href="https://example.com/page2">Page 2</a>
                </body>
            </html>
        '''
        mock_get.return_value = mock_response

        # Run crawler + processor pipeline
        result = self.crawler.fetch("http://mocked-url.com")

        # Save only the URLs extracted to file
        urls = result.get("urls", []) if result else []
        with open(self.output_file, "w") as f:
            for url in urls:
                f.write(url + "\n")

        # Assert file was created and has extracted URLs
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r") as f:
            content = f.read()
            self.assertIn("https://example.com/page1", content)
            self.assertIn("https://example.com/page2", content)

    #def tearDown(self):
        # Clean up generated file
        #if os.path.exists(self.output_file):
            #os.remove(self.output_file)

if __name__ == "__main__":
    unittest.main()