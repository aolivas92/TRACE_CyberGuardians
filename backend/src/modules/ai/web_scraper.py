import requests
from bs4 import BeautifulSoup
import time
import csv

class WebScraper:
    """
    Web scraper to extract text content from web pages.
    
    Attributes:
        urls (list): List of URLs to scrape.
    """
    
    def __init__(self, urls):
        """
        Initialize with list of URLs.
        
        Args:
            urls (list): List of URLs to scrape.
        """
        self.urls = urls

    def scrape_pages(self):
        """
        Scrape text content from web pages.
        
        Returns:
            list: List of tuples with ID, content, and URL.
        """
        results = []
        for i, url in enumerate(self.urls, 1):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract text from p, h1, h2, h3, and span tags
                text = ' '.join([tag.get_text() for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'span'])])
                results.append((i, text, url))
                time.sleep(1)  # Be polite to servers
            except Exception as e:
                print(f"Error scraping {url}: {e}")
        return results

    def generate_csv(self, filename):
        """
        Generate CSV file with scraped data.
        
        Args:
            filename (str): Output CSV filename.
        """
        data = self.scrape_pages()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['id', 'content', 'url'])  # Header
            csv_writer.writerows(data)
        print(f"CSV file '{filename}' has been generated.")