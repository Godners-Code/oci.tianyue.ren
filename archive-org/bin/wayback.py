#!/usr/bin/env python3
import os, time, logging
from datetime import datetime

from wayback_log import setup_logging
from wayback_site import crawl_and_archive
from wayback_list import load_urls

MAX_DEPTH = 5
MAX_URLS = 200
DELAY = 8

WAYBACK_ETC = os.path.expanduser("~/etc")
USER_AGENT = open(os.path.join(WAYBACK_ETC, "wayback.user-agent"), 'r').read().strip()

LIST_FILE=os.path.join(WAYBACK_ETC, "wayback.list")
LOG_FILE = "/var/log/archive-org/wayback.log"

def get_now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main(logger: logging.Logger):
    logger.info("========================= WAYBACK ARCHIVER START =========================")
    logger.info(f"Start Time: {get_now()}, List File: {LIST_FILE}")

    urls = load_urls(LIST_FILE, logger)
    if not urls:
        logger.warning("List File is Empty, NO URLs to Process.")
        return

    logger.info(f"Found {len(urls)} Base URLs\n")

    total_success = 0
    for i, base_url in enumerate(urls, 1):
        logger.info(f"[{1}/{len(urls)}] {base_url} ====================")
        success = crawl_and_archive(base_url, MAX_URLS, MAX_DEPTH, USER_AGENT, logger)
        total_success += success
        if i < len(urls):
            logger.info(f"Waiting {DELAY} Seconds before Next Site ...\n")
            time.sleep(DELAY * 2)

    logger.info("\nAll Processing Completed.")
    logger.info(f"Total End Time: {get_now()}")
    logger.info(f"Total Successfully Archived Pages: {total_success}")
    logger.info("========================= WAYBACK ARCHIVER END =========================\n")

if __name__ == "__main__":
    main(setup_logging(LOG_FILE))

