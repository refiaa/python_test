import logging
import requests
import base64
from http_client.http_client import HttpClient
from typing import Dict, Any, List

logging.basicConfig(level=logging.DEBUG)

class XssScanner:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client
        self.payloads = self.load_payloads('./payloads/xss_payloads.txt')

    def load_payloads(self, path: str) -> List[str]:
        with open(path, 'r') as file:
            return [base64.b64encode(line.strip().encode()).decode() for line in file if line.strip()]

    def scan(self, endpoint: str, param: str) -> Dict[str, Any]:
        for payload in self.payloads:
            decoded_payload = base64.b64decode(payload).decode()
            params = {param: decoded_payload}
            logging.debug(f"Attempting XSS with URL: {self.http_client.base_url}/{endpoint} and params: {params}")
            try:
                response = self.http_client.get(endpoint, params=params, timeout=10)
                response_text = response.text[:1000]
                if decoded_payload in response.text:
                    logging.info(f"Vulnerable endpoint: {endpoint}, Parameter: {param}, Payload: {decoded_payload}")
                    return {
                        "endpoint": endpoint, 
                        "param": param, 
                        "payload": decoded_payload, 
                        "vulnerable": True, 
                        "status_code": response.status_code, 
                        "response": response_text
                    }
            except requests.exceptions.HTTPError as e:
                logging.error(f"HTTP error during XSS scan: {e}")
                if e.response.status_code == 403:
                    logging.error(f"Access forbidden: {endpoint}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Request exception occurred: {e}")
        return {
            "endpoint": endpoint, 
            "param": param, 
            "vulnerable": False, 
            "status_code": None, 
            "response": None
        }
