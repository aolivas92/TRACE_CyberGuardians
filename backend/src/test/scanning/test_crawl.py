#!/usr/bin/env python3
import asyncio
import os
import json
import shutil
import unittest
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time
import sys
from pathlib import Path

# Add the parent directory to sys.path to import the crawler modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the crawler modules
from src.modules.scanning.CrawlerManager import CrawlerManager
from src.modules.scanning.crawler_response import CrawlerResponseProcessor

# Create a directory for test files
TEST_DIR = Path("test_crawler")
TEST_DIR.mkdir(exist_ok=True)

# Create test HTML pages
def create_test_pages():
    # Create index.html
    with open(TEST_DIR / "index.html", "w") as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Page</title>
            <link href="styles.css" rel="stylesheet">
            <script src="script.js"></script>
        </head>
        <body>
            <h1>Test Crawler Page</h1>
            <p>This is a test page for the crawler.</p>
            <img src="image.jpg" alt="Test Image">
            <a href="page1.html">Link to Page 1</a>
            <a href="page2.html">Link to Page 2</a>
            <a href="subdir/page3.html">Link to Page 3</a>
            <a href="http://example.com">External Link</a>
            <a href="mailto:test@example.com">Email Link</a>
            <form action="process.php" method="post">
                <input type="text" name="test">
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
        """)
    
    # Create page1.html
    with open(TEST_DIR / "page1.html", "w") as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Page 1</title>
        </head>
        <body>
            <h1>Page 1</h1>
            <p>This is page 1.</p>
            <a href="index.html">Back to Index</a>
            <a href="page2.html">Link to Page 2</a>
        </body>
        </html>
        """)
    
    # Create page2.html
    with open(TEST_DIR / "page2.html", "w") as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Page 2</title>
        </head>
        <body>
            <h1>Page 2</h1>
            <p>This is page 2.</p>
            <a href="index.html">Back to Index</a>
            <a href="page1.html">Link to Page 1</a>
        </body>
        </html>
        """)
    
    # Create subdirectory and page3.html
    (TEST_DIR / "subdir").mkdir(exist_ok=True)
    with open(TEST_DIR / "subdir" / "page3.html", "w") as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Page 3</title>
        </head>
        <body>
            <h1>Page 3</h1>
            <p>This is page 3 in a subdirectory.</p>
            <a href="../index.html">Back to Index</a>
        </body>
        </html>
        """)
    
    # Create empty files for other referenced resources
    (TEST_DIR / "styles.css").touch()
    (TEST_DIR / "script.js").touch()
    (TEST_DIR / "image.jpg").touch()
    (TEST_DIR / "process.php").touch()

# Start a simple HTTP server
def start_server():
    os.chdir(TEST_DIR)
    server = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server

class TestCrawler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create test pages and start server
        create_test_pages()
        cls.server = start_server()
        time.sleep(1)  # Give the server time to start
    
    @classmethod
    def tearDownClass(cls):
        # Stop server and clean up
        cls.server.shutdown()
        cls.server.server_close()
        os.chdir("..")
        shutil.rmtree(TEST_DIR)
        
        # Clean up output files
        for file in ["extracted_urls_tree.txt", "crawler_table_data.json", "raw_html.txt"]:
            if os.path.exists(file):
                os.remove(file)
    
    def test_crawler_response_processor(self):
        # Test the CrawlerResponseProcessor directly
        processor = CrawlerResponseProcessor()
        
        abs_path = os.path.abspath("test_crawler")[:-(len(str(TEST_DIR)))]
        with open(abs_path + "\\index.html", "r") as f:
            html_content = f.read()
        
        result = processor.process_response(html_content, "http://localhost:8000/")
        
        # Verify the result
        self.assertEqual(result["processor"], "CrawlerResponseProcessor")
        self.assertIsInstance(result["extracted_urls"], list)
        self.assertGreaterEqual(result["count"], 8)  # Should have at least 8 URLs
        
        # Verify that the tree file was created
        self.assertTrue(os.path.exists("extracted_urls_tree.txt"))
        
        # Read the tree file and verify it contains URLs
        with open("extracted_urls_tree.txt", "r") as f:
            tree_content = f.read()
        self.assertIn("http://localhost:8000/", tree_content)
    
    async def async_test_crawler_manager(self):
        # Test the CrawlerManager
        manager = CrawlerManager()
        manager.configure_crawler(
            target_url="http://localhost:8000/index.html",
            depth=2,
            limit=10,
            user_agent="Mozilla/5.0 Test",
            delay=100,  # 100ms delay
            proxy="",
            excluded_urls="http://example.com,mailto:test@example.com"
        )
        
        results = await manager.start_crawl()
        
        # Verify the results
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 1)
        
        # Verify that the output JSON file was created
        self.assertTrue(os.path.exists("crawler_table_data.json"))
        
        # Read the JSON file and verify it contains the expected data
        with open("crawler_table_data.json", "r") as f:
            table_data = json.load(f)
        
        self.assertIsInstance(table_data, list)
        self.assertGreaterEqual(len(table_data), 1)
        
                    # Verify the structure of table data entries
        for entry in table_data:
            self.assertIn("id", entry)
            self.assertIn("url", entry)
            self.assertIn("parentUrl", entry)
            self.assertIn("title", entry)
            self.assertIn("wordCount", entry)
            self.assertIn("charCount", entry)
            self.assertIn("linksFound", entry)
            self.assertIn("error", entry)
        
        # Check if we crawled the main page and some subpages
        urls = [entry["url"] for entry in table_data]
        self.assertIn("http://localhost:8000/index.html", urls)
        
        # At least one of the linked pages should be crawled
        linked_pages = ["http://localhost:8000/page1.html", 
                       "http://localhost:8000/page2.html", 
                       "http://localhost:8000/subdir/page3.html"]
        self.assertTrue(any(page in urls for page in linked_pages))
        
        # Check that excluded URLs were not crawled
        self.assertNotIn("http://example.com", urls)
    
    def test_crawler_manager(self):
        # Run the async test with asyncio
        asyncio.run(self.async_test_crawler_manager())

if __name__ == "__main__":
    unittest.main()