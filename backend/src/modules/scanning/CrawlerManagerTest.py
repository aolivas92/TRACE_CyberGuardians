import unittest
from unittest.mock import patch, MagicMock
from CrawlerManager import CrawlerManager

class TestCrawlerManager(unittest.TestCase):
    def setUp(self):
        self.crawler = CrawlerManager()
    
    def test_configure_crawler(self):
        self.crawler.configure_crawler("http://crawler.com", 2, 100, "Mozilla/5.0", 1, "proxy:8080")
        self.assertIsNotNone(self.crawler.config)
        self.assertEqual(self.crawler.config["target_url"], "http://crawler.com")
    
    def test_start_crawl_without_configuration(self):
        with self.assertRaises(ValueError) as context:
            self.crawler.start_crawl()
        self.assertEqual(str(context.exception), "Crawler not configured")
    
    def test_process_response_with_invalid_data(self):
        with self.assertRaises(ValueError) as context:
            self.crawler.process_response("Invalid")
        self.assertEqual(str(context.exception), "Dictionary")
    
    def test_brute_force_directories_with_no_wordlist(self):
        with self.assertRaises(ValueError) as context:
            self.crawler.brute_force_directories("http://crawler.com", [])
        self.assertEqual(str(context.exception), "No wordlist")
    
    @patch("builtins.open", new_callable=MagicMock)
    @patch("os.makedirs")
    
    def test_save_results(self, mock_makedirs, mock_open):
        self.crawler.results = {"test": "data"}
        self.crawler.save_results()
        mock_makedirs.assert_called_once_with("database", exist_ok=True)
        mock_open.assert_called_once_with("database/crawler_results.json", "w")
    
    def test_reset_crawler(self):
        self.crawler.results = {"some": "data"}
        self.crawler.config = {"some": "config"}
        self.crawler.reset_crawler()
        self.assertEqual(self.crawler.results, {})
        self.assertEqual(self.crawler.config, {})

unittest.main()