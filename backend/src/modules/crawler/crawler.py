# crawler.py
import requests

class Crawler:
    def __init__(self, response_processor, logger):
        self._response_processor = response_processor
        self._logger = logger

    def fetch(self, url):
        try:
            self._logger.info(f"Fetching URL: {url}")
            response = requests.get(url)
            response.raise_for_status()
            return self._response_processor.process_response(response)
        except Exception as e:
            self._logger.error(f"Crawler fetch failed: {e}")
            return None