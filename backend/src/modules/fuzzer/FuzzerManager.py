import os
import time
import logging
from typing import List, Dict
from src.modules.fuzzer.FuzzerResponseProcessor import FuzzerResponseProcessor
from src.modules.fuzzer.HTTPClient import AsyncHttpClient

log_path = os.path.join(os.path.dirname(__file__), "fuzzing.log")
logging.basicConfig(
    filename=log_path,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class MockResponse:
    def __init__(self, url, status, text):
        self.url = url
        self.status_code = status
        self.text = text

class FuzzerManager:
    def __init__(self, http_client=None):
        self.config = {}
        self.response_processor = FuzzerResponseProcessor()
        self.http_client = http_client or AsyncHttpClient()
        self.request_count = 0
        self.start_time = None
        self.end_time = None

    def configure_fuzzing(self, target_url: str, http_method: str, headers: Dict =None, cookies: Dict = None, proxy: str =None, body_template: str = None, parameters: List[str] = None, payloads=None):
        """
        Accepts and stores fuzzing configuration.
        """
        if not target_url or not http_method or not parameters or not payloads:
            raise ValueError("Missing required fuzzing configuration parameters.")
        
        if isinstance(payloads, str) and os.path.isfile(payloads):
            with open(payloads, "r", encoding="utf-8") as f:
                payloads = [line.strip() for line in f if line.strip()]
        
        if not isinstance(payloads, list) or not payloads:
            raise ValueError("Payloads must be a non-empty list or a valid file path.")

        self.config = {
            "target_url": target_url,
            "http_method": http_method,
            "headers": headers or {},
            "cookies": cookies or {},
            "proxy": proxy,
            "body_template": body_template or {},
            "parameters": parameters,
            "payloads": payloads
        }

    async def start_fuzzing(self):
        self.start_time = time.perf_counter()
        """
        Begins the fuzzing process using the provided configuration.
        """
        target_url = self.config.get("target_url")
        http_method = self.config.get("http_method", "GET").upper()
        headers = self.config.get("headers", {})
        cookies = self.config.get("cookies", {})
        proxy = self.config.get("proxy")
        body_template = self.config.get("body_template", {})
        parameters = self.config.get("parameters", [])
        payloads = self.config.get("payloads", [])

        logging.info("Fuzzing started with %d payloads across %d parameter(s)", len(payloads), len(parameters))

        proxies = {"http": proxy, "https": proxy} if proxy else None

        for payload in payloads:
            for param in parameters:
                modified_body = body_template.copy()
                modified_body[param] = payload
                logging.info("Sending %s request to %s with %s=%s", http_method, target_url, param, payload)
                try:
                    response = await self.http_client.send(
                        method=http_method,
                        url=target_url,
                        headers=headers,
                        cookies=cookies,
                        data=modified_body if http_method in ["POST", "PUT"] else None,
                        params=modified_body if http_method == "GET" else None,
                        proxy=proxies,
                        timeout=5.0
                    )
                    mock = MockResponse(response["url"], response["status"], response["text"])
                    self.response_processor.process_response(mock)
                    logging.info("Received response %d from %s", response["status"], response["url"])
                    self.request_count += 1
                except Exception as e:
                    print(f"[!] Request error {e}")
        
        self.end_time = time.perf_counter()
    
    def get_metrics(self):
        total_time = self.end_time - self.start_time if self.start_time and self.end_time else 0
        rps = self.request_count / total_time if total_time > 0 else 0

        return {
            "running_time": total_time,
            "processed_requests": self.request_count,
            "filtered_requests": len(self.response_processor.get_filtered_results()),
            "requests_per_second": rps
        }
    
    def get_filtered_results(self):
        return self.response_processor.get_filtered_results()
