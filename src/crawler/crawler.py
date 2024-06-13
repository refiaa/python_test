import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.DEBUG)

class WebCrawler:
    def __init__(self, base_url: str, max_depth: int = 2):
        self.base_url = base_url
        self.visited = set()
        self.max_depth = max_depth
        self.start_paths = ['/', '/index.html', '/home', '/main', '/default']

    def crawl(self):
        for path in self.start_paths:
            self._crawl_path(path, 0)

    def _crawl_path(self, path: str, depth: int):
        if depth > self.max_depth:
            return
        full_url = urljoin(self.base_url, path)
        if full_url in self.visited:
            return
        self.visited.add(full_url)

        try:
            response = requests.get(full_url)
            response.raise_for_status()
            logging.debug(f"Accessing {full_url}")

            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                full_href = urljoin(self.base_url, href)
                if self.is_valid_url(full_href):
                    logging.debug(f"Found link: {full_href}")
                    self._crawl_path(full_href, depth + 1)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error accessing {full_url}: {e}")

    def is_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https') and (not parsed.netloc or parsed.netloc == urlparse(self.base_url).netloc)

    def get_results(self):
        return self.visited
