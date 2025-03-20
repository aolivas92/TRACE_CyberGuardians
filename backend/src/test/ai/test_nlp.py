import unittest
from unittest.mock import patch, mock_open
import io
from src.modules.ai.nlp import NLP


class TestNLP(unittest.TestCase):
    """Test cases for the NLP class."""

    def setUp(self):
        """Set up test fixtures."""
        self.nlp = NLP()
        self.test_csv_path = "test_data.csv"

        # Sample CSV data for testing
        self.sample_csv_content = (
            "id,content,url\n"
            "1,The quick brown fox jumps over the lazy dog,http://example.com\n"
            "2,This is an example and a test,http://test.com\n"
        )

        self.expected_cleaned_content = (
            "id,content,url\n"
            "1,quick brown fox jumps over lazy dog,http://example.com\n"
            "2,This is example test,http://test.com\n"
        )

    def test_init_default_stopwords(self):
        """Test that the default stopwords are set correctly."""
        nlp = NLP()
        self.assertEqual(nlp.stop_words, {"the", "or", "and", "a", "an"})

    def test_init_custom_stopwords(self):
        """Test initialization with custom stopwords."""
        custom_stopwords = {"is", "a", "test"}
        nlp = NLP(custom_stopwords)
        self.assertEqual(nlp.stop_words, custom_stopwords)

    @patch("os.path.exists")
    def test_subroutine_file_not_found(self, mock_exists):
        """Test that FileNotFoundError is raised when the file doesn't exist."""
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            self.nlp.subroutine(self.test_csv_path)

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_read_csv_missing_required_columns(self, mock_file, mock_exists):
        """Test that ValueError is raised when required columns are missing."""
        mock_exists.return_value = True
        mock_file.return_value.__enter__.return_value = io.StringIO(
            "column1,column2\n1,value1,value2\n"
        )

        with self.assertRaises(ValueError):
            self.nlp._read_csv(self.test_csv_path)

    @patch("os.path.exists")
    @patch("builtins.open")
    def test_subroutine_integration(self, mock_open_file, mock_exists):
        """Test the complete subroutine flow with mocked file operations."""
        mock_exists.return_value = True

        # Mock the file operations
        mock_read = mock_open(read_data=self.sample_csv_content)
        mock_write = mock_open()

        # Configure the mock to return different file handles for read and write
        mock_open_file.side_effect = [mock_read.return_value, mock_write.return_value]

        # Run the subroutine
        self.nlp.subroutine(self.test_csv_path)

        # Verify the file was opened for reading and writing
        mock_open_file.assert_any_call(self.test_csv_path, "r", encoding="utf-8")
        mock_open_file.assert_any_call(
            self.test_csv_path, "w", newline="", encoding="utf-8"
        )

        # Check if write_csv was called with the correct arguments
        # This is a bit complex to verify directly with mock_open, so we'll test the methods separately

    def test_read_csv_valid_file(self):
        """Test reading a valid CSV file."""
        with patch("builtins.open", mock_open(read_data=self.sample_csv_content)):
            result = self.nlp._read_csv(self.test_csv_path)

            # Check fieldnames
            self.assertEqual(result["fieldnames"], ["id", "content", "url"])

            # Check rows
            self.assertEqual(len(result["rows"]), 2)
            self.assertEqual(result["rows"][0]["id"], "1")
            self.assertEqual(
                result["rows"][0]["content"],
                "The quick brown fox jumps over the lazy dog",
            )

    def test_process_content(self):
        """Test processing content to remove stopwords."""
        # Prepare test data
        test_data = {
            "fieldnames": ["id", "content", "url"],
            "rows": [
                {
                    "id": "1",
                    "content": "The quick brown fox jumps over the lazy dog",
                    "url": "http://example.com",
                },
                {
                    "id": "2",
                    "content": "This is an example and a test",
                    "url": "http://test.com",
                },
            ],
        }

        # Process the content
        cleaned_rows = self.nlp._process_content(test_data)

        # Check the results
        self.assertEqual(
            cleaned_rows[0]["content"], "quick brown fox jumps over lazy dog"
        )
        self.assertEqual(cleaned_rows[1]["content"], "This is example test")

    def test_write_csv(self):
        """Test writing processed rows to a CSV file."""
        # Prepare test data
        rows = [
            {
                "id": "1",
                "content": "quick brown fox jumps over lazy dog",
                "url": "http://example.com",
            },
            {"id": "2", "content": "This is example test", "url": "http://test.com"},
        ]

        # Mock file operations
        mock_file = mock_open()

        with patch("builtins.open", mock_file):
            self.nlp._write_csv(self.test_csv_path, rows)

            # Check that the file was opened for writing
            mock_file.assert_called_once_with(
                self.test_csv_path, "w", newline="", encoding="utf-8"
            )

            # It's difficult to check the exact CSV content with mock_open
            # In real testing, we would use a temporary file and read it back

    def test_empty_content_field(self):
        """Test handling of rows with empty content field."""
        # Prepare test data
        test_data = {
            "fieldnames": ["id", "content", "url"],
            "rows": [
                {
                    "id": "1",
                    "content": "",  # Empty content
                    "url": "http://example.com",
                }
            ],
        }

        # Process the content
        cleaned_rows = self.nlp._process_content(test_data)

        # Check the results - empty content should remain empty
        self.assertEqual(cleaned_rows[0]["content"], "")

    def test_missing_content_field(self):
        """Test handling of rows with missing content field."""
        # Prepare test data
        test_data = {
            "fieldnames": ["id", "url"],  # No content field
            "rows": [
                {
                    "id": "1",
                    "url": "http://example.com",
                    # No content key
                }
            ],
        }

        # Process the content
        cleaned_rows = self.nlp._process_content(test_data)

        # Check the results - missing content should be treated as empty
        self.assertEqual(cleaned_rows[0].get("content", ""), "")

    @patch("os.path.exists")
    @patch("builtins.open")
    @patch("builtins.print")
    def test_subroutine_print_message(self, mock_print, mock_open_file, mock_exists):
        """Test that the success message is printed."""
        mock_exists.return_value = True

        # Mock the file operations
        mock_read = mock_open(read_data=self.sample_csv_content)
        mock_write = mock_open()

        # Configure the mock to return different file handles for read and write
        mock_open_file.side_effect = [mock_read.return_value, mock_write.return_value]

        # Run the subroutine
        self.nlp.subroutine(self.test_csv_path)

        # Verify the success message is printed
        mock_print.assert_called_once_with(
            f"Cleaned CSV '{self.test_csv_path}' has been generated."
        )


if __name__ == "__main__":
    unittest.main()
