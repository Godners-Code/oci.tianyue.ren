#!/usr/bin/env python3
from urllib.parse import urlparse

def get_base_domain(url: str) -> str:
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path.split('/')[0]
    if ':' in domain:
        domian = domain.split(':')[0]
    return domain.lower()

def is_same_domain(url: str, base_domain: str) -> bool:
    domain = get_base_domain(url)
    return domain == base_domain or domain.endswith('.' + base_domain)


