#!/usr/bin/env python3
import os, logging, shutil
from pathlib import Path

from setup_logging import setup_logging
from load_config import load_config
from mirror_page_util import ensure_dirs, cleanup_temp
from mirror_page_downloader import download_artifacts_for_repo
from mirror_page_extractor import extract_artifact

CONF_FILE = os.path.expanduser("~/etc/mirror_page.toml")
LOG_FILE = Path("/var/log/openresty/mirror_page.log")

REPO_LSIT = []; MAIN_REPO = ""; PAGES_HOME = Path('~/html').expanduser()
GITHUB_TOKEN = ""; MAX_SEARCH = 1

def start_progress(config: dict, logger: logging.Logger):
    logger.info("Starting Mirror Page Artiface Download Progress")
    ensure_dirs(config)

    global REPO_LIST, MAIN_REPO, PAGES_HOME, GITHUB_TOKEN, MAX_SEARCH
    MAIN_REPO = config["MAIN_REPO"]
    PAGES_HOME = Path(config["PAGES_HOME"]).expanduser()
    GITHUB_TOKEN = config.get("GITHUB_TOKEN", '')
    MAX_SEARCH = config.get('MAX_SEARCH', 1)
    REPO_LIST = config.get("REPO_LIST", [])
    if not REPO_LIST:
        logger.error("No Repositories Found in Config File")
        return

def process_artifact_path(repo_url: str, logger: logging.Logger):
    artifact_path, repo_name = download_artifacts_for_repo(repo_url, GITHUB_TOKEN, MAX_SEARCH, logger)
    if artifact_path == None or not Path(artifact_path):
        logger.warning(f"No Artifact Downloaded for {repo_url}")
        return
    save_dir = PAGES_HOME / repo_name
    extract_artifact(artifact_path, save_dir, logger)
    logger.info(f"Successfully Processed {repo_url}")
    
def process_main_repo(logger: logging.Logger):
    main_save_dir = PAGES_HOME / MAIN_REPO
    if not main_save_dir.exists():
        logger.warning(f" Main Repository Directory NOT Found: {main_save_dir}")
        return
    try:
        target_dir = PAGES_HOME
        for item in main_save_dir.iterdir():
            dest = target_dir / item.name
            if item.is_dir():
                if dest.exists() and dest.is_dir():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)
        logger.info("Main Repository Files Copied to Root")
    except Exception as e:
        logger.warning(f"Main Repo Copy Failed: {e}")

def mirror_page_main(logger: logging.Logger = None):    
    if logger is None:
        logger = setup_logging(LOG_FILE)
    config = load_config(CONF_FILE, logger)
    start_progress(config, logger)
    processed = 0
    for repo_url in REPO_LIST:
        processed += 1
        logger.info(f"[{processed} / {len(REPO_LIST)}] Processing Repository: {repo_url}")
        try:
            process_artifact_path(repo_url, logger)
            pass
        except Exception as e:
            logger.error(f"Failed to Process {repo_url}: {e}")
            continue
    process_main_repo(logger)
    logger.info("Mirror Page Process Completed.")

if __name__ == "__main__":
    mirror_page_main()
