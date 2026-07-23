#!/usr/bin/env python3
import logging, requests, concurrent.futures, time

from wayback_links import extract_links
from wayback_domain import get_base_domain
from wayback_save import archive_single_url

def crawl_and_archive(start_url: str ,max_urls: int, max_depth: int, user_agent: str, logger: logging.Logger) -> int:
    base_domain = get_base_domain(start_url)
    visited = set()
    to_visit = [(start_url, 0)]
    archived_count = 0

    logger.info(f"Starting Crawl for Domain: {base_domain}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {}

        while to_visit and archived_count < max_urls:
            url, depth = to_visit.pop(0)
            if url in visited:
                continue
            visited.add(url)

            logger.info(f"Processing [{archived_count + 1}] Depth {depth}: {url}")

            future = executor.submit(archive_single_url, url, user_agent, logger)
            future_to_url[future] = url

            if depth < max_depth:
                try:
                    response = requests.get(url, headers={"User-Agent": user_agent}, timeout=30)
                    response.raise_for_status()
                    links = extract_links(response.text, url, base_domain)
                    for link in links:
                        if link not in visited:
                            to_visit.append((link, depth + 1))
                except Exception as e:
                    logger.warning(f"Failed to Extract Links from {url}: {e}")

            time.sleep(1)

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                if future.result():
                    archived_count += 1
            except Exception as e:
                logger.error(f"Error Archiving {url}: {e}")

    logger.info("Crawl Completed for {base_domain}. Archived {archived_count} Pages.")
    return archived_count            
    
