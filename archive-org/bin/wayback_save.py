#!/usr/bin/env python3
import time, logging, requests
from waybackpy import WaybackMachineSaveAPI
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def archive_single_url(url: str, user_agent: str, logger: logging.Logger) -> bool:
    logger.info(f"Submitting to Archive: {url}")
    start_time = time.time()
    try:
        session = requests.Session()
        retries = Retry(
                total=5,
                backoff_factor=2,
                status_forcelist=[429, 500, 502, 503, 504, 111],
                allowed_methods=["GET", "POST"]
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        save_api = WaybackMachineSaveAPI(url=url, user_agent=user_agent)
        archived_url = save_api.save()

        elapsed = time.time() - start_time
        logger.info(f"Successfully Archived: Time Taken {elapsed:.3f} Seconds, {url} -> {archived_url}")
        return True
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Failed to Archive: Time Taken {elapsed:.3f} Seconds, {url} -> {e}")

        if "Connection refused" in str(e) or "Errno 111" in str(e):
            logger.warning("Connection Refused Detected. Sleeping 30 Second before Next Attempt ...")
            time.sleep(30)

        return False
    finally:
        try:
            session.close()
        except:
            pass


