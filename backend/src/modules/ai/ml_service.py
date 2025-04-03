import csv

from credential_generator import Credential_Generator
from web_scraper import WebScraper
from nlp import NLP


def main():
    # FIXME: Chaange for getting wordlist and stuff
    urls = []
    scraper = WebScraper(urls=urls)
    scraped_file = "scraper_output.csv"
    scraper.scrape_pages(scraped_file)

    nlp = NLP()
    nlp.subroutine(scraped_file)

    generator = Credential_Generator(csv_path=scraped_file)
    credentials = generator.generate_credentials(count=10)

    credential_file = "generated_credentials.csv"
    with open(credential_file, "w", newline="", encoding="utf-8") as f:
        field_names = ["username", "password"]
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for username, password in credentials:
            writer.writerow({"username": username, "password": password})


if __name__ == "__main__":
    main()
