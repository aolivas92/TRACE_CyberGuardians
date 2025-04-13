import os
import time
import logging
from typing import List, Dict
from dbf_response_processor import ResponseProcessor
from httpmock import AsyncHttpClient

log_path = os.path.join(os.path.dirname(__file__), "directory_bruteforce.log")
logging.basicConfig(
    filename=log_path,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class MockResponse:
    def __init__(self, url: str, status: int, text: str):
        self.url = url
        self.status_code = status
        self.text = text
        self.payload = None
        self.error = False

class DirectoryBruteForceManager:
    def __init__(self, http_client: AsyncHttpClient = None) -> None:
        self.config = {}
        self.response_processor = ResponseProcessor()
        self.http_client = http_client or AsyncHttpClient()
        self.request_count = 0
        self.attempt_limit = -1
        self.start_time = None
        self.end_time = None

    def configure_scan(
        self,
        target_url: str,
        wordlist: List[str],
        top_dir: str = '',
        hide_status: List[int] = None,
        show_only_status: List[int] = None,
        length_filter: int = None,
        headers: Dict[str, str] = None,
        attempt_limit: int = -1
    ) -> None:
        if not target_url or not wordlist:
            raise ValueError("Missing required configuration parameters.")

        self.config = {
            "target_url": target_url.rstrip('/'),
            "wordlist": wordlist,
            "top_dir": top_dir.strip('/'),
            "hide_status": hide_status or [],
            "show_only_status": show_only_status or [],
            "length_filter": length_filter,
            "headers": headers or {}
        }
        self.attempt_limit = attempt_limit
        self.response_processor.set_filters(show_only_status or [200], hide_status or [], length_filter)

    async def start_scan(self) -> None:
        self.start_time = time.perf_counter()
        target = self.config["target_url"]
        top = self.config["top_dir"]
        wordlist = self.config["wordlist"]
        headers = self.config["headers"]

        for word in wordlist:
            path = f"{top}/{word}" if top else word
            full_url = f"{target}/{path}"
            try:
                response = await self.http_client.send(
                    method="GET",
                    url=full_url,
                    headers=headers
                )
                mock = MockResponse(response["url"], response["status"], response["text"])
                mock.payload = word
                mock.error = response["status"] not in [200, 403]
                self.response_processor.process_response(mock)
                logging.info("Scanned %s [%d]", full_url, response["status"])
                self.request_count += 1
            except Exception as e:
                logging.error("Request error for %s: %s", full_url, str(e))
                error_response = MockResponse(full_url, 0, str(e))
                error_response.payload = word
                error_response.error = True
                self.response_processor.process_response(error_response)
        self.end_time = time.perf_counter()

    def get_metrics(self) -> Dict[str, float]:
        total_time = self.end_time - self.start_time if self.start_time and self.end_time else 0
        rps = self.request_count / total_time if total_time > 0 else 0
        return {
            "running_time": total_time,
            "processed_requests": self.request_count,
            "filtered_requests": len(self.response_processor.get_filtered_results()),
            "requests_per_second": rps
        }

    def get_filtered_results(self) -> List[Dict]:
        return self.response_processor.get_filtered_results()
