import asyncio
import pytest
from unittest.mock import AsyncMock, patch
from src.modules.scanning.crawler_manager import crawler_manager

@pytest.mark.asyncio
async def test_crawler_manager():
    mock_http_client = AsyncMock()
    mock_http_client.get.side_effect = ["<html><body><a href='/level1/page1'>Page 1</a></body></html>",
        "<html><body>No more links here.</body></html>"]
    with patch("crawler_manager.RealHTTPClient", return_value=mock_http_client):
        manager = crawler_manager()
        manager.configure_crawler(target_url="http://localhost:5000/", depth=1, limit=10, user_agent="Mozilla/5.0", delay=0, proxy=None,)
        results = await manager.start_crawl()
    assert len(results) == 2
    assert results[0]["url"] == "http://localhost:5000/"
    assert results[1]["url"].endswith("/level1/page1")