import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util.ssl_ import create_urllib3_context
from typing import Dict, Any
import ssl

class SslAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        context = create_urllib3_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        self.ssl_context = context
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().proxy_manager_for(*args, **kwargs)

class HttpClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

        adapter = SslAdapter()
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)

    def get(self, endpoint: str, params: Dict[str, Any] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response

    def post(self, endpoint: str, data: Dict[str, Any] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response
