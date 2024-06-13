import logging
from typing import Dict, Any
from http_client.http_client import HttpClient

logging.basicConfig(level=logging.DEBUG)

class SqlInjectionScanner:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client
        self.payloads = ["' OR '1'='1", "'; DROP TABLE users; --"]

    def scan(self, endpoint: str, param: str) -> Dict[str, Any]:
        for payload in self.payloads:
            params = {param: payload}
            logging.debug(f"Attempting SQL Injection with URL: {self.http_client.base_url}/{endpoint} and params: {params}")
            response = self.http_client.get(endpoint, params)
            if "error" not in response.text:
                return {"endpoint": endpoint, "param": param, "payload": payload, "vulnerable": True}
        return {"endpoint": endpoint, "param": param, "vulnerable": False}
