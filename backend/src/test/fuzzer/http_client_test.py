# http_client_test.py

import asyncio
import aiohttp
import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from src.modules.fuzzer.http_client import AsyncHttpClient

class TestAsyncHttpClient(unittest.IsolatedAsyncioTestCase):
    @patch("aiohttp.ClientSession")
    async def test_send_successful_get_request(self, mock_client_session):
        mock_response = AsyncMock()
        mock_response.url = "http://test.com"
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="Success")
        mock_request_ctx = AsyncMock()
        mock_request_ctx.__aenter__.return_value = mock_response
        mock_session_instance = MagicMock()
        mock_session_instance.request.return_value = mock_request_ctx
        mock_client_session.return_value.__aenter__.return_value = mock_session_instance
        client = AsyncHttpClient()
        result = await client.send(method="GET", url="http://test.com")
        self.assertEqual(result["url"], "http://test.com")
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["text"], "Success")

    @patch("aiohttp.ClientSession")
    async def test_send_request_exception(self, mock_client_session):
        mock_session_instance = MagicMock()
        mock_session_instance.request.side_effect = Exception("Connection failed")
        mock_client_session.return_value.__aenter__.return_value = mock_session_instance
        client = AsyncHttpClient()
        result = await client.send(method="GET", url="http://test.com")
        self.assertEqual(result["url"], "http://test.com")
        self.assertIsNone(result["status"])
        self.assertIn("Connection failed", result["text"])

unittest.main()