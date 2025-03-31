# test_crawler_response.py
import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.modules.scanning.crawler_response import CrawlerResponseProcessor

class TestCrawlerResponseProcessor(unittest.TestCase):
    """Test suite for the CrawlerResponseProcessor class."""

    def setUp(self):
        self.processor = CrawlerResponseProcessor()

    @patch("src.modules.scanning.crawler_response.BeautifulSoup")
    @patch("src.modules.scanning.crawler_response.open", new_callable=mock_open)
    def test_process_response(self, mock_file, mock_soup):
        """Test extracting URLs and saving tree structure."""

        # Mocking HTML tags
        soup_instance = MagicMock()
        soup_instance.find_all.side_effect = [
            [MagicMock(**{"__getitem__.return_value": "/a"})],  # <a>
            [MagicMock(**{"__getitem__.return_value": "/b"})],  # <link>
            [MagicMock(**{"__getitem__.return_value": "/c.js"})],  # <script>
            [MagicMock(**{"__getitem__.return_value": "/d.png"})],  # <img>
            [MagicMock(**{"__getitem__.return_value": "/submit"})]  # <form>
        ]
        mock_soup.return_value = soup_instance

        # Act
        result = self.processor.process_response("<html></html>", "https://example.com")

        # Assert
        self.assertEqual(result["processor"], "CrawlerResponseProcessor")
        self.assertEqual(result["count"], 5)
        self.assertIn("/a", result["extracted_urls"])
        self.assertIn("/b", result["extracted_urls"])
        mock_file.assert_called_with("extracted_urls_tree.txt", "w", encoding="utf-8")

if __name__ == "__main__":
    unittest.main()