import random
import re
from collections import defaultdict
import csv
import requests
from bs4 import BeautifulSoup
import time

class MarkovChain:
    def __init__(self, order=2):
        self.order = order
        self.model = defaultdict(list)

    def train(self, data):
        for item in data:
            for i in range(len(item) - self.order):
                state = item[i:i+self.order]
                next_char = item[i+self.order]
                self.model[state].append(next_char)

    def generate(self, length):
        current = random.choice(list(self.model.keys()))
        result = current
        for _ in range(length - self.order):
            if current not in self.model:
                break
            next_char = random.choice(self.model[current])
            result += next_char
            current = result[-self.order:]
        return result

#Web scraper functions and will pull something out of the URLs provided.
class WebScraper:
    def __init__(self, urls):
        self.urls = urls

    def scrape_pages(self):
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
        data = self.scrape_pages()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['id', 'content', 'url'])  # Header
            csv_writer.writerows(data)
        print(f"CSV file '{filename}' has been generated.")

class CredentialGenerator:
    def __init__(self, web_text_csv, wordlist_file):
        self.web_text_csv = web_text_csv
        self.wordlist_file = wordlist_file
        self.web_text = ""
        self.wordlists = []
        self.username_model = MarkovChain(order=2)
        self.password_model = MarkovChain(order=3)

    def load_data(self):
        # Load web text from CSV
        with open(self.web_text_csv, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                if len(row) >= 2:
                    self.web_text += row[1] + " "

        # Load wordlists from file
        with open(self.wordlist_file, 'r', encoding='utf-8') as f:
            self.wordlists = [line.strip() for line in f if line.strip()]

    def preprocess_text(self, text):
        return re.findall(r'\w+', text.lower())

    def train_models(self):
        self.load_data()
        username_data = self.preprocess_text(self.web_text) + self.wordlists
        password_data = [word for word in self.wordlists]

        self.username_model.train(username_data)
        self.password_model.train(password_data)

    def generate_username(self):
        base = self.username_model.generate(random.randint(5, 8))
        return f"{base}{random.randint(1, 999)}"

    def generate_password(self):
        base = self.password_model.generate(random.randint(10, 14))
        enhanced = base.capitalize()
        enhanced = f"{enhanced}{random.choice('!@#$%^&*')}{random.randint(0, 9)}"
        return enhanced

    def generate_credentials(self, count=10):
        credentials = []
        for _ in range(count):
            username = self.generate_username()
            password = self.generate_password()
            credentials.append((username, password))
        return credentials

urls = [
    #"http://192.168.1.123/admin/index.php", #Seb's Pi-Hole
    "http://127.0.0.1/server/login.php", #James server
    #"http://127.0.0.1/server/index.php", #James server
    "https://en.wikipedia.org/wiki/System_administrator",
    #"https://www.redhat.com/en/topics/linux/what-is-a-system-administrator",
    #"https://www.airshows.pa.hq.af.mil/gaframework/Presentation/security.cfm"
]

scraper = WebScraper(urls)
scraper.generate_csv("web_text.csv")

# Use generated CSV and a wordlist file for credential generation
# For now: these files are HARDCODED and need to be located in the
# same dir; can be written over!!
web_text_csv = "web_text.csv"
wordlist_file = "wordlist.txt"

generator = CredentialGenerator(web_text_csv, wordlist_file)
generator.train_models()
credentials = generator.generate_credentials(150)

for username, password in credentials:
    print(f"Username: {username}, Password: {password}")
