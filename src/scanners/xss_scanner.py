import requests

from typing import Dict, Any
from http_client.http_client import HttpClient

class XssScanner:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client
        self.payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]

    def scan(self, endpoint: str, param: str) -> Dict[str, Any]:
        for payload in self.payloads:
            params = {param: payload}
            response = self.http_client.get(endpoint, params)
            if payload in response.text:
                return {"endpoint": endpoint, "param": param, "payload": payload, "vulnerable": True}
        return {"endpoint": endpoint, "param": param, "vulnerable": False}