import logging
import requests

from http_client.http_client import HttpClient
from typing import Dict, Any

logging.basicConfig(level=logging.DEBUG)

class XssScanner:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client
        self.payloads = [
            "<script>alert('XSS')</script>",
            "\";alert('XSS');//",
            "';alert('XSS');//",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
        ]

    def scan(self, endpoint: str, param: str) -> Dict[str, Any]:
        for payload in self.payloads:
            params = {param: payload}
            logging.debug(f"Attempting XSS with URL: {self.http_client.base_url}/{endpoint} and params: {params}")
            try:
                response = self.http_client.get(endpoint, params)
                if payload in response.text:
                    return {"endpoint": endpoint, "param": param, "payload": payload, "vulnerable": True}
            except requests.exceptions.HTTPError as e:
                logging.error(f"HTTP error during XSS scan: {e}")
                if e.response.status_code == 403:
                    logging.error(f"Access forbidden: {endpoint}")
        return {"endpoint": endpoint, "param": param, "vulnerable": False}
