import os
import json
import time
import random
import requests
import re

# Crawler Manager

class CrawlerManager:
    def __init__(self):
        self.results = {}
        self.config = {}
        self.wordlist = []
    
    def configure_crawler(self, target_url: str, depth: int, limit: int, user_agent: str, delay: int, proxy: str) -> None:
        self.config = {"target_url": target_url,
                       "depth": depth,
                       "limit": limit,
                       "user_agent": user_agent,
                       "delay": delay,
                       "proxy": proxy}
        
    def start_crawl(self) -> None:
        if not self.config:
            raise ValueError("Crawler not configured")
        
        print("Simulated crawl")
        directories = ["/", "/home", "/var", "/usr", "/etc"]
        connections = [(random.choice(directories), f"{random.choice(directories)}/subdir_{i}") for i in range(5)]
        self.results["directories"] = directories
        self.results["connections"] = connections
        
        time.sleep(2)

    def process_response(self, response: dict) -> None:
        if not isinstance(response, dict):
            raise ValueError("Response should be a dictionary")
        self.results["processed_response"] = response

    def save_results(self, fastapi_url: str) -> None:
        try:
            response = requests.post(fastapi_url, json=self.results)
            if response.status_code == 200:
                print("Results sent to FastAPI successfully.")
            else:
                print(f"Failed - Status: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

    def reset_crawler(self) -> None:
        self.results = {}
        self.config = {}
        print("Crawler reset")

# Response Processor

class Logger:
    def info(self, msg): 
        print(f"INFO: {msg}")
    
    def warning(self, msg): 
        print(f"WARNING: {msg}")
    
    def error(self, msg): 
        print(f"ERROR: {msg}")
    
    def debug(self, msg): 
        print(f"DEBUG: {msg}")

class Parser:
    def parse(self, raw_content):
        urls = re.findall(r'https?://[^\s"\'>]+', str(raw_content))
        return {"urls": urls}
    
class Cleaner: 
    def clean(self, parsed_data):
        parsed_data["cleaned"] = True
        return parsed_data

class Validator:
    def is_valid(self, cleaned_data):
        return True if cleaned_data else False

class CrawlerResponseProcessor:
    def __init__(self, logger, parser, cleaner, validator):
        self.logger = logger
        self.parser = parser
        self.cleaner = cleaner
        self.validator = validator

    def process_response(self, raw_content: str) -> dict | None:
        if not raw_content:
            self.logger.error("InvalidResponse: raw_content is empty.")
            raise ValueError("InvalidResponse: raw_content is empty.")
    
        self.logger.info("Processing raw crawler response.")
        parsed_data = self._parse_content(raw_content)
        cleaned_data = self._clean_data(parsed_data)
        if self._validate_data(cleaned_data):
            self.logger.info("Processed response successfully.")
            return cleaned_data
        else:
            self.logger.warning("Validation failed for processed response.")
            return None
        
    def _parse_content(self, raw_content: str) -> dict:
        self.logger.debug("Analyzing raw HTML for useful data.")
        return self.parser.parse(raw_content)

    def _clean_data(self, parsed_data: dict) -> dict:
        self.logger.debug("Normalizing and cleaning parsed data.")
        return self.cleaner.clean(parsed_data)
    
    def _validate_data(self, cleaned_data: dict) -> bool:
        self.logger.debug("Validating the cleaned data.")
        return self.validator.is_valid(cleaned_data)

# Integration
crawler_manager = CrawlerManager()
crawler_manager.configure_crawler(target_url="http://crawler.com", depth=2, limit=100, user_agent="Mozilla/5.0", delay=1, proxy="")
crawler_manager.start_crawl()
raw_content = "Here are some URLs: http://crawler1.com http://crawler2.com"
logger = Logger()
parser = Parser()
cleaner = Cleaner()
validator = Validator()
response_processor = CrawlerResponseProcessor(logger, parser, cleaner, validator)
processed_data = response_processor.process_response(raw_content)
if processed_data:
    print(f"Processed Data: {processed_data}")
    crawler_manager.process_response(processed_data)
    crawler_manager.save_results("http://crawlerapi.com")
crawler_manager.reset_crawler()
