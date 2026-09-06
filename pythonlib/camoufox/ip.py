from ipaddress import ip_address
import re
from dataclasses import dataclass
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from typing import Dict, Optional, Tuple

import requests

from .exceptions import InvalidIP, InvalidProxy

"""
Helpers to find the user's public IP address for geolocation.
"""


@dataclass
class Proxy:
    """
    Stores proxy information.
    """

    server: str
    username: Optional[str] = None
    password: Optional[str] = None
    bypass: Optional[str] = None

    @staticmethod
    def parse_server(server: str) -> Tuple[str, str, Optional[str]]:
        """
        Parses the proxy server string.
        """
        proxy_match = re.match(r'^(?:(?P<schema>\w+)://)?(?P<url>.*?)(?:\:(?P<port>\d+))?$', server)
        if not proxy_match:
            raise InvalidProxy(f"Invalid proxy server: {server}")
        return proxy_match['schema'], proxy_match['url'], proxy_match['port']

    def as_string(self) -> str:
        schema, url, port = self.parse_server(self.server)
        if not schema:
            schema = 'http'
        result = f"{schema}://"
        if self.username:
            result += f"{self.username}"
            if self.password:
                result += f":{self.password}"
            result += "@"

        result += url
        if port:
            result += f":{port}"
        return result

    @staticmethod
    def as_requests_proxy(proxy_string: str) -> Dict[str, str]:
        """
        Converts the proxy to a requests proxy dictionary.
        """
        return {
            'http': proxy_string,
            'https': proxy_string,
        }


@lru_cache(128, typed=True)
def valid_ipv4(ip: str) -> bool:
    try:
        return ip_address(ip).version == 4
    except ValueError:
        return False


@lru_cache(128, typed=True)
def valid_ipv6(ip: str) -> bool:
    try:
        return ip_address(ip).version == 6
    except ValueError:
        return False


def validate_ip(ip: str) -> None:
    if not valid_ipv4(ip) and not valid_ipv6(ip):
        raise InvalidIP(f"Invalid IP address: {ip}")


# A bounded process-wide pool lets the first successful request return without
# waiting for unrelated providers. Running requests retain their own timeout.
_IP_EXECUTOR = ThreadPoolExecutor(max_workers=6, thread_name_prefix='camoufox-ip')

def public_ip(proxy: Optional[str] = None) -> str:
    """
    Sends requests to multiple public IP APIs in parallel and returns the first valid response.
    """
    URLS = [
        "https://api.ipify.org",
        "https://checkip.amazonaws.com",
        "https://ipinfo.io/ip",
        "https://icanhazip.com",
        "https://ifconfig.co/ip",
        "https://ipecho.net/plain",
    ]

    proxies = Proxy.as_requests_proxy(proxy) if proxy else None

    def fetch_ip(url):
        try:
            with requests.get(url, proxies=proxies, timeout=5) as resp:
                resp.raise_for_status()
                ip = resp.text.strip()
                validate_ip(ip)
                return ip
        except Exception:
            return None

    # Proxy endpoints may rotate between launches; never cache an exit by URL.
    futures = [_IP_EXECUTOR.submit(fetch_ip, url) for url in URLS]
    try:
        for future in as_completed(futures, timeout=6):
            result = future.result()
            if result:
                return result
    except TimeoutError:
        pass
    finally:
        for future in futures:
            future.cancel()

    raise InvalidIP("Failed to get IP address from any service")
