# mock_http

import aiohttp

class RealHTTPClient:
    """
    RealHTTPClient is responsible for performing HTTP GET requests asynchronously. It uses the aiohttp library to send requests and retrieve responses.

    Attributes:
        None
    
    Methods:
        get(url: str, headers: dict = None, proxy: str = None) -> str:
            
    Notes:
        None
    """

    async def get(self, url, headers=None, proxy=None):
        """
        get sends an HTTP GET request to the specified URL and returns the response content.

        Args:
            url (str): The URL to which the GET request is sent.
            headers (dict, optional): The headers to include in the request.
            proxy (str, optional): The proxy to use for the request.

        Returns:
            str: The content of the response returned from the server.

        Raises:
            None

        @requires url != "";
        @ensures response == string.
        """
        async with aiohttp.ClientSession(headers=headers) as session:
            if proxy:
                async with session.get(url, proxy=proxy) as response:
                    return await response.text()
            else:
                async with session.get(url) as response:
                    return await response.text()