import requests
import logging

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

logging.basicConfig(level=logging.DEBUG)

class WebCrawler:
    def __init__(self, base_url: str, wordlist_path: str, max_depth: int = 2):
        self.base_url = base_url
        self.visited = set()
        self.max_depth = max_depth
        self.login_page = None
        self.paths = self.load_wordlist(wordlist_path)

    def load_wordlist(self, path: str):
        with open(path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    def crawl(self):
        for path in self.paths:
            self._crawl_path(path, 0)

    def _crawl_path(self, path: str, depth: int):
        if depth > self.max_depth or self.login_page:
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
            if self._is_login_page(soup, full_url):
                self.login_page = full_url
                logging.debug(f"Login page found: {full_url}")
                return

            for link in soup.find_all('a', href=True):
                href = link.get('href')
                full_href = urljoin(self.base_url, href)
                if self.is_valid_url(full_href) and not self.is_excluded(full_href):
                    logging.debug(f"Found link: {full_href}")
                    self._crawl_path(full_href, depth + 1)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error accessing {full_url}: {e}")

    def _is_login_page(self, soup: BeautifulSoup, url: str) -> bool:
        form = soup.find('form')
        if form:
            for input_tag in form.find_all('input'):
                if input_tag.get('type') in ['text', 'password']:
                    return True
        if any(keyword in url.lower() for keyword in ['login', 'signin', 'auth']):
            return True
        return False

    def is_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https') and (not parsed.netloc or parsed.netloc == urlparse(self.base_url).netloc)

    def is_excluded(self, url: str) -> bool:
        return any(url.endswith(ext) for ext in ['.php', '.jpg', '.jpeg', '.png', '.gif', '.css', '.js'])

    def get_results(self):
        return self.visited

    def get_login_page(self):
        return self.login_page
