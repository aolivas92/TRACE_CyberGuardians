import re

class logger: 
    def info(self, msg): print(f"INFO: {msg}")
    def warning(self, msg): print(f"WARNING: {msg}")
    def error(self, msg): print(f"ERROR: {msg}")
    def debug(self, msg): print(f"DEBUG: {msg}")

class parser:
    def parse(self, raw_content):
        urls = re.findall(r'https?://[^\s"\'>]+', str(raw_content))
        return {"urls": urls}
    
class cleaner: 
    def clean(self, parsed_data):
        parsed_data["cleaned"] = True
        return parsed_data

class validator:
    def is_valid(self, cleaned_data):
        return True if cleaned_data else False

class CrawlerResponseProcessor:
    """
    The CrawlerResponseProcessor processes HTTP responses obtained by the Crawler class. It extracts content, parses it,
    cleans it, validates it, and returns structured data.

    """

    def __init__(self, logger, parser, cleaner, validator):
        self.logger = logger()
        self.parser = parser()
        self.cleaner = cleaner()
        self.validator = validator()

    def process_response(self, raw_content: str) -> dict | None:
        """
        Processes the web crawler response through extraction, parsing, cleaning, and validation.

        """
    
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
        """
        Parses raw content into structured data.

        """
        self.logger.debug("Analyzing raw HTML for useful data.")
        return self.parser.parse(raw_content)

    def _clean_data(self, parsed_data: dict) -> dict:
        """
        Cleans and normalizes parsed data.

        """
        self.logger.debug("Normalizing and cleaning parsed data.")
        return self.cleaner.clean(parsed_data)
    
    def _validate_data(self, cleaned_data: dict) -> bool:
        """
        Validates cleaned data.

        """
        self.logger.debug("Validating the cleaned data.")
        return self.validator.is_valid(cleaned_data)
    
    def send_filtered_urls(self, cleaned_data: dict, http_client) -> None:
        filtered_urls = cleaned_data.get("urls", [])
        valid_urls = [url for url in filtered_urls if self._is_valid_url(url)]

        if not valid_urls:
            self.logger.warning("No valid URLs to send.")
            return

        self.logger.info(f"Sending {len(valid_urls)} filtered URLs to HTTP client.")
        for url in valid_urls:
            http_client.send(url)
        self.logger.debug("Updated HTTP client's request queue.")

    def _is_valid_url(self, url: str) -> bool:
        return url.startswith("http://") or url.startswith("https://")