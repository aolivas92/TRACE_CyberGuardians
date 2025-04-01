import aiohttp

class RealHTTPClient:
    async def get(self, url, headers=None, proxy=None):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                return await response.text()