# http_client.py
from typing import List, Dict, Any
import aiohttp

class AsyncHttpClient:
    """
    AsyncHttpClient represents an asynchronous HTTP client for sending requests using aiohttp.

    Attributes:
        None

    Methods:
        async def send(
            method: str,
            url: str,
            headers: Optional[Dict[str, str]] = None,
            cookies: Optional[Dict[str, str]] = None,
            data: Optional[Any] = None,
            params: Optional[Dict[str, str]] = None,
            proxy: Optional[str] = None,
            timeout: int = 5
        ) -> Dict[str, Any]

    Notes:
        This client is designed to be used for async operations and works well with asyncio-based fuzzing or crawling tools.
    """

    async def send(
        self,
        method: str,
        url: str,
        headers: List[str] = None,
        cookies: List[str] = None,
        data: List[str] = None,
        params: List[str] = None,
        proxy: List[str] = None,
        timeout: int = 5
    ) -> List[str]:
        """
        send() asynchronously sends an HTTP request and returns a dictionary containing the response.

        Args:
            method (str): The HTTP method to use (GET, POST, PUT, DELETE, PATCH).
            url (str): The full URL to send the request to.
            headers (Optional[Dict[str, str]]): HTTP headers to include in the request.
            cookies (Optional[Dict[str, str]]): Cookies to include in the request.
            data (Optional[Any]): Data to send in the body of the request for POST/PUT.
            params (Optional[Dict[str, str]]): Query parameters to include for GET requests.
            proxy (Optional[str]): Proxy URL to use for the request.
            timeout (int): Request timeout in seconds.

        Returns:
            Dict[str, Any]: A dictionary containing: url (str): The URL of the response.
            status (int or None): The HTTP status code.
            text (str): The body of the response or the error message.

        Raises:
            Exception: If an exception occurs while sending the request.

        @requires isinstance(method, str) and method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"];
        @requires isinstance(url, str) and url.startswith("http");
        @requires timeout > 0;
        @ensures isinstance(result, dict);
        @ensures "url" in result and "status" in result and "text" in result;
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