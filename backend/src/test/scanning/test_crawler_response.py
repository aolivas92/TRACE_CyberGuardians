# test_crawler_response.py
import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.modules.scanning.crawler_response import CrawlerResponseProcessor
from src.modules.scanning.crawler_response import BST

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

class TestBST(unittest.TestCase):
    """Test suite for the BST class."""

    def setUp(self):
        self.bst = BST()


    def test_insert_tree(self):
        root = self.bst.insert(None, "http://example.com")
        self.assertEqual(root.value, "http://example.com")
        self.assertEqual(self.bst.root, root)

    def test_build_tree(self):
        """Test building the tree structure."""
        urls = {"http://example.com/page1", "http://example.com/page2", "http://example.com/page3"}
        self.bst.build_tree("http://example.com", urls)
        self.assertEqual(len(self.bst.root.children), 3)
        child_values = [child.value.strip() for child in self.bst.root.children]
        self.assertIn("http://example.com/page1", child_values)
        self.assertIn("http://example.com/page2", child_values)
        self.assertIn("http://example.com/page3", child_values)

    @patch("src.modules.scanning.crawler_response.open", new_callable=mock_open)
    def test_save_tree_to_file(self, mock_file):
        """Test saving the tree structure to a file."""

        self.bst.build_tree("http://example.com", {"http://example.com/page1"})

        self.bst.save_tree_to_file("test_tree.txt")
        mock_file.assert_called_with("test_tree.txt", "w", encoding="utf-8")
        handle = mock_file()
        write_calls = handle.write.call_args_list
        expected_calls = [
            "http://example.com\n",
            "  http://example.com/page1\n"
        ]
        for call, expected in zip(write_calls, expected_calls):
            self.assertEqual(call.args[0], expected)
if __name__ == "__main__":
    unittest.main()