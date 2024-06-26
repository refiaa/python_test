import logging
import requests

from http_client.http_client import HttpClient
from typing import Dict, Any, List
from reporter.ssrf_dts_reporter import SsrfDtsReporter

logging.basicConfig(level=logging.DEBUG)

class DirectoryTraversalScanner:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client
        self.payloads = self.load_payloads('./payloads/directory_traversal_payloads.txt')
        self.reporter = SsrfDtsReporter()

    def load_payloads(self, path: str) -> List[str]:
        with open(path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    def scan(self, endpoint: str, param: str) -> Dict[str, Any]:
        for payload in self.payloads:
            params = {param: payload}
            logging.debug(f"Attempting Directory Traversal with URL: {self.http_client.base_url}/{endpoint} and params: {params}")
            try:
                response = self.http_client.get(endpoint, params=params, timeout=10)
                response_text = response.text[:1000]
                if "root:x" in response.text or "boot.ini" in response.text:
                    logging.info(f"Vulnerable endpoint: {endpoint}, Parameter: {param}, Payload: {payload}")
                    self.reporter.add_vulnerability(endpoint, "Directory Traversal", True, {
                        "param": param,
                        "payload": payload,
                        "status_code": response.status_code,
                        "response": response_text
                    })
                    return {
                        "endpoint": endpoint,
                        "param": param,
                        "payload": payload,
                        "vulnerable": True,
                        "status_code": response.status_code,
                        "response": response_text
                    }
            except requests.exceptions.HTTPError as e:
                logging.error(f"HTTP error during Directory Traversal scan: {e}")
                if e.response.status_code == 403:
                    logging.error(f"Access forbidden: {endpoint}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Request exception occurred: {e}")
        self.reporter.add_vulnerability(endpoint, "Directory Traversal", False, {
            "param": param,
            "payload": None,
            "status_code": None,
            "response": None
        })
        return {
            "endpoint": endpoint,
            "param": param,
            "vulnerable": False,
            "status_code": None,
            "response": None
        }