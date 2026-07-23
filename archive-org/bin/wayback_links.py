#!/usr/bin/env python3
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

from wayback_domain import is_same_domain

def extract_links(html: str, base_url: str, base_domain: str) -> set[str]:
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)
        if parsed.scheme in ('http', 'https') and is_same_domain(full_url, base_domain):
            clean_url = parsed._replace(fragment='').geturl()
            links.add(clean_url)
    return links

