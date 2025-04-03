import logging
import json
from typing import List

class FuzzerResponseProcessor:
    def __init__(self):
        self.responses = []
        self.status_code_filter = [200, 403, 500]
        self.hide_codes = []
        self.length_threshold = 0

    def set_filters(self, status_filter: List[int], hide_codes: List[int] = [], length_threshold: int = 0):
        self.status_code_filter = status_filter
        self.hide_codes = hide_codes
        self.length_threshold = length_threshold

    def process_response(self, response):
        """
        Analyze and store response if it matches filters.
        """
        status = response.status_code
        content_length = len(response.text)

        if status in self.hide_codes:
            return
        
        logging.info("Filtered response: %s [%d bytes]", response.url, content_length)
        if status in self.status_code_filter and content_length >= self.length_threshold:
            self.responses.append({
                "id": len(self.responses) + 1,
                "response": status,
                "url": response.url,
                "payload": getattr(response, "payload", None),
                "length": content_length,
                "snippet": response.text[:200],
                "error": getattr(response, "error", False)
            })

    def get_filtered_results(self):
        return self.responses
