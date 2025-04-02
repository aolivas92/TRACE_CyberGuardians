import unittest
import csv
from src.modules.ai.nlp import NLP
from src.modules.ai.credential_generator import Credential_Generator
from src.modules.ai.web_scraper import WebScraper


class TestTRACEIntegration(unittest.TestCase):
 
    def setUp(self):
        self.mock_html = "https://crawler-test.com/"
        self.test_filename = None
        scraper = WebScraper([self.mock_html])
        csv_file = scraper.scrape_pages()
        if csv_file:
            self.test_filename = scraper.filename
 
    def test_web_scraper_to_csv(self):
        
        self.assertIsNotNone(self.test_filename)
        
        with open(self.test_filename, "r", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            data = [row[-1] for row in reader]

        for entry in data:
            self.assertIn(entry, self.mock_html)
       
        
    
    def test_web_scraper_to_nlp(self):
        if self.test_filename is None:
            self.skipTest("Skipping NLP test: No CSV file generated.")
        nlp = NLP()
        nlp.subroutine(self.test_filename)
        self.assertIsNotNone(self.test_filename)
        with open(self.test_filename, "r", encoding="utf-8") as f:
            nlp_html = f.read()

        self.assertNotEqual(nlp_html, self.mock_html)
        
    
    def test_nlp_to_credential_generator(self):
        if self.test_filename is None:
            self.skipTest("Skipping Credential test: No CSV file generated.")
        cred_gen = Credential_Generator(csv_path=self.test_filename)
        results = cred_gen.generate_credentials(count = 10)
        q = results
        while len(q) > 0:
            tail = q.pop()
            self.assertNotIn(q, results)
        for cred in results:
            self.assertGreaterEqual(cred[0], cred_gen.min_username_length) 
            self.assertGreaterEqual(cred[1], cred_gen.min_password_length)
        print(results)
        
            

if __name__ == '__main__':
    unittest.main()