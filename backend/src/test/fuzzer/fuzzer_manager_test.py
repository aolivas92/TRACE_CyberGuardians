# fuzzer_manager_test.py

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock
from src.modules.fuzzer.fuzzer_manager import FuzzerManager

class TestFuzzerManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_http_client = MagicMock()
        self.mock_http_client.send = AsyncMock(return_value={
            "url": "http://test.com",
            "status": 200,
            "text": "OK"
        })
        self.fuzzer = FuzzerManager(http_client=self.mock_http_client)
        self.config = {
            "target_url": "http://test.com",
            "http_method": "POST",
            "headers": {"User-Agent": "MockAgent"},
            "cookies": {"session": "fake"},
            "proxy": None,
            "body_template": {"username": "admin"},
            "parameters": ["username"],
            "payloads": ["test1", "test2"]
        }

    def test_configure_fuzzing_valid(self):
        self.fuzzer.configure_fuzzing(
            target_url=self.config["target_url"],
            http_method=self.config["http_method"],
            headers=self.config["headers"],
            cookies=self.config["cookies"],
            proxy=self.config["proxy"],
            body_template=self.config["body_template"],
            parameters=self.config["parameters"],
            payloads=self.config["payloads"]
        )
        self.assertIn("target_url", self.fuzzer.config)
        self.assertEqual(self.fuzzer.config["payloads"], ["test1", "test2"])

    async def test_start_fuzzing_with_mock(self):
        self.fuzzer.configure_fuzzing(
            target_url=self.config["target_url"],
            http_method=self.config["http_method"],
            headers=self.config["headers"],
            cookies=self.config["cookies"],
            proxy=self.config["proxy"],
            body_template=self.config["body_template"],
            parameters=self.config["parameters"],
            payloads=self.config["payloads"]
        )
        await self.fuzzer.start_fuzzing()
        self.assertEqual(self.fuzzer.request_count, 2)
        metrics = self.fuzzer.get_metrics()
        self.assertGreaterEqual(metrics["running_time"], 0)
        self.assertEqual(metrics["processed_requests"], 2)
        filtered_results = self.fuzzer.get_filtered_results()
        self.assertIsInstance(filtered_results, list)
        self.assertEqual(len(filtered_results), 2)
        self.assertEqual(filtered_results[0]["response"], 200)
        self.assertEqual(filtered_results[0]["url"], "http://test.com")

unittest.main()