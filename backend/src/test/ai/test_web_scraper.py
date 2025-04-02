import unittest
from unittest.mock import patch, MagicMock, mock_open
import asyncio
import aiohttp

from src.modules.ai.web_scraper import WebScraper

class TestWebScraper(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.test_urls = ["http://example.com", "http://test.com"]
        self.scraper = WebScraper(self.test_urls, concurrency=2)
    
    def test_init(self):
        """Test initialization of WebScraper"""
        self.assertEqual(self.scraper.urls, self.test_urls)
        self.assertEqual(self.scraper.concurrency, 2)
    
    def test_extract_text_content(self):
        """Test the _extract_text_content method with various HTML elements"""
        # Test HTML with different elements
        html = """
        <html>
            <body>
                <h1>Main Title</h1>
                <p>This is a paragraph</p>
                <div class="content-box important">
                    <h2>Subtitle</h2>
                    <span>Some span text</span>
                    <img alt="Logo Alt Text" src="logo.png">
                </div>
                <label>Form Label</label>
                <div aria-label="Accessibility Label">Accessible Text</div>
                <div aria-labelledby="label-id">Referenced Text</div>
                <div id="label-id">Label Text</div>
            </body>
        </html>
        """
        
        result = self.scraper._extract_text_content(html)
        
        # Verify that all expected content is extracted
        self.assertIn("Main Title", result)
        self.assertIn("This is a paragraph", result)
        self.assertIn("Subtitle", result)
        self.assertIn("Some span text", result)
        self.assertIn("Logo Alt Text", result)
        self.assertIn("Form Label", result)
        self.assertIn("Accessibility Label", result)
        self.assertIn("Label Text", result)
        self.assertIn("content-box important", result)
    
    @patch('aiohttp.ClientSession.get')
    async def test_fetch_url(self, mock_get):
        """Test the _fetch_url method"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.text = MagicMock(return_value=asyncio.Future())
        mock_response.text.return_value.set_result("<html>Test content</html>")
        
        # Mock the context manager
        mock_get.return_value.__aenter__.return_value = mock_response
        
        result = await self.scraper._fetch_url("http://example.com")
        
        # Verify the result
        self.assertEqual(result, "<html>Test content</html>")
        mock_get.assert_called_once_with("http://example.com")
    
    @patch('aiohttp.ClientSession.get')
    async def test_fetch_url_error(self, mock_get):
        """Test error handling in _fetch_url method"""
        # Mock to raise an exception
        mock_get.side_effect = aiohttp.ClientError("Connection error")
        
        with patch('builtins.print') as mock_print:
            result = await self.scraper._fetch_url("http://example.com")
            
            # Verify error handling
            mock_print.assert_called_once()
            self.assertIsNone(result)
    
    @patch("src.modules.ai.web_scraper.WebScraper._fetch_url")
    @patch("src.modules.ai.web_scraper.WebScraper._extract_text_content")
    async def test_scrape_pages_async(self, mock_extract, mock_fetch):
        """Test the _scrape_pages_async method"""
        # Setup mocks
        future1, future2 = asyncio.Future(), asyncio.Future()
        mock_fetch.side_effect = [future1, future2]
        future1.set_result("<html>Page 1</html>")
        future2.set_result("<html>Page 2</html>")
        
        mock_extract.side_effect = ["Content from page 1", "Content from page 2"]
        
        # Execute the method
        results = await self.scraper._scrape_pages_async()
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], (1, "Content from page 1", "http://example.com"))
        self.assertEqual(results[1], (2, "Content from page 2", "http://test.com"))
        
        # Verify the mocks were called correctly
        self.assertEqual(mock_fetch.call_count, 2)
        self.assertEqual(mock_extract.call_count, 2)
    
    @patch('asyncio.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_scrape_pages(self, mock_file, mock_run):
        """Test the scrape_pages method"""
        # Setup mock for asyncio.run to return test data
        mock_run.return_value = [
            (1, "Content from page 1", "http://example.com"),
            (2, "Content from page 2", "http://test.com")
        ]
        
        # Execute the method
        result = self.scraper.scrape_pages("test_output.csv")
        
        # Verify asyncio.run was called with the correct coroutine
        mock_run.assert_called_once()
        
        # Verify the file was opened correctly
        mock_file.assert_called_once_with('test_output.csv', 'w', newline='', encoding='utf-8')
        
        # Verify the CSV writer was used correctly
        handle = mock_file()
        writer = handle.write
        writer.assert_called()  # The CSV writer writes to the file
        
        # Verify the return value
        self.assertEqual(result, mock_run.return_value)

if __name__ == '__main__':
    unittest.main()