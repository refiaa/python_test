from http_client.http_client import HttpClient
from typing import Dict, Any

class AttackExecutor:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def execute_attack(self, vulnerability: Dict[str, Any]) -> str:
        if vulnerability["vulnerable"]:
            response = self.http_client.post(vulnerability['endpoint'], data={"username": "admin", "password": vulnerability["payload"]})
            if response.status_code == 200:
                return "Admin access granted!"
        return "Attack failed."