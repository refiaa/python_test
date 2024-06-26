import requests
import ssl
import logging

from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util.ssl_ import create_urllib3_context
from typing import Dict, Any

logging.basicConfig(level=logging.DEBUG)

class SslAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        context = create_urllib3_context()
        context.check_hostname = False
        context.set_ciphers('DEFAULT@SECLEVEL=1')
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

    def set_cookies(self, cookies: Dict[str, str]):
        self.session.cookies.update(cookies)

    def get(self, endpoint: str, params: Dict[str, Any] = None, timeout: int = 10) -> requests.Response:
        url = endpoint if endpoint.startswith("http") else f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            response = self.session.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.SSLError as e:
            logging.error(f"SSL error occurred: {e}")
            raise
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            if e.response.status_code == 403:
                logging.error(f"Access forbidden: {url}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception occurred: {e}")
            raise

    def post(self, endpoint: str, data: Dict[str, Any] = None, timeout: int = 10) -> requests.Response:
        url = endpoint if endpoint.startswith("http") else f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            response = self.session.post(url, data=data, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.SSLError as e:
            logging.error(f"SSL error occurred: {e}")
            raise
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            if e.response.status_code == 403:
                logging.error(f"Access forbidden: {url}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception occurred: {e}")
            raise
