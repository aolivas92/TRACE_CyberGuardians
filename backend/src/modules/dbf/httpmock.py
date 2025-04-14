import aiohttp
from typing import Optional, Dict, Any

class AsyncHttpClient:

    async def send(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 5
    ) -> Dict[str, any]:
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.request(
                    method=method.upper(),
                    url=url,
                    timeout=timeout
                ) as response:
                    return {
                        "url": str(response.url),
                        "status": response.status,
                        "text": await response.text()
                    }
        except Exception as e:
            print(f"[AsyncHttpClient] Error sending request to {url}: {e}")
            return {
                "url": url,
                "status": None,
                "text": str(e)
            }