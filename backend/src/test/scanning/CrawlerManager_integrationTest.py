import json
import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from src.modules.scanning.CrawlerManager import CrawlerManager

@pytest.mark.asyncio
async def test_crawler_manager_integration():
    crawler_manager = CrawlerManager()
    crawler_manager.configure_crawler(target_url="https://crawler.com/", depth=2, limit=100, user_agent="Mozilla/5.0", delay=1, proxy="")
    assert crawler_manager.config["target_url"] == "https://crawler.com/"
    with patch("crawler_manager.ResponseProcessor") as MockRP:
        mock_rp = MockRP.return_value
        mock_rp.run = AsyncMock()
        mock_rp.export_tree = AsyncMock()
        mock_rp.tree = {"home": ["about", "contact"]}
        mock_rp.external_links = ["https://external.com/"]
        mock_rp.run.return_value = {"tree": {"home": ["about", "contact"]}, "external_links": ["https://external.com"]}
        with patch.object(crawler_manager, 'fetch', return_value="<html>Dummy HTML content</html>") as mock_fetch:
            await crawler_manager.start_crawl()
        assert "processed_response" in crawler_manager.results
        assert len(crawler_manager.results["processed_response"]) > 0
        processed_response = crawler_manager.results["processed_response"][0]
        assert "tree" in processed_response
        assert "external_links" in processed_response
        with patch("crawler_manager.requests.post") as mock_post:
            mock_response = mock_post.return_value
            mock_response.status_code = 200
            await crawler_manager.store_results("http://crawlerapi.com/")
            mock_post.assert_called_once()
    crawler_manager.reset_crawler()
    assert not crawler_manager.results
    assert not crawler_manager.config
    assert not crawler_manager.crawl_tree