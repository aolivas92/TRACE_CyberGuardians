import aiohttp

class AsyncHttpClient:
    async def send(self, method, url, headers=None, cookies=None, data=None, params=None, proxy=None, timeout=5):
        """
        Asynchronously sends an HTTP request and returns a dict with the result.
        """
        try:
            async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
                async with session.request(
                    method=method.upper(),
                    url=url,
                    params=params if method.upper() == "GET" else None,
                    data=data if method.upper() in ["POST", "PUT"] else None,
                    proxy=proxy,
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
