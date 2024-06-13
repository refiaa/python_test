import logging
import requests

from typing import Dict, Any
from http_client.http_client import HttpClient

logging.basicConfig(level=logging.DEBUG)

class DirectoryBruteForcer:
    def __init__(self, http_client: HttpClient, wordlist: str):
        self.http_client = http_client
        with open(wordlist, 'r') as f:
            self.directories = f.read().splitlines()

    def brute_force(self) -> Dict[str, Any]:
        results = []
        for directory in self.directories:
            logging.debug(f"Attempting to access directory: {self.http_client.base_url}/{directory}")
            try:
                response = self.http_client.get(directory)
                if response.status_code == 200:
                    logging.debug(f"Found directory: {directory}")
                    results.append({"directory": directory, "status": "found"})
                else:
                    logging.debug(f"Directory not found: {directory} (Status code: {response.status_code})")
            except requests.exceptions.HTTPError as e:
                if e.response.status_code != 404:
                    logging.error(f"Error accessing {directory}: {e}")
        return results