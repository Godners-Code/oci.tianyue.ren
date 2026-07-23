#!/usr/bin/env python3
import os, logging
from pathlib import Path

from setup_logging import setup_logging
from load_config import load_config
from sync_repo_loader import load_repos, get_repo_name_from_url
from sync_repo_git import ensure_repo_exists, git_pull, git_pull_force
from sync_repo_show import show_commits, show_actions

CONF_FILE = os.path.expanduser("~/etc/sync_repo.toml")
LOG_FILE = Path("/var/log/openresty/sync_repo.log")

SHOW_COMMITS = 1; SHOW_ACTIONS = 1; REPO_LIST = []
GITHUB_HOME = os.path.expanduser("~/GitHub"); GITHUB_TOKEN = ""

def start_progress(logger: logging.Logger):
    config = load_config(CONF_FILE, logger)
    global SHOW_COMMITS, SHOW_ACTIONS, GITHUB_HOME, GITHUB_TOKEN, REPO_LIST
    SHOW_COMMITS = config.get('SHOW_COMMITS', 1)
    SHOW_ACTIONS = config.get('SHOW_ACTIONS', 1)
    GITHUB_HOME = Path(os.path.expanduser(str(config.get('GITHUB_HOME', '~/GitHub'))))
    GITHUB_HOME.mkdir(parents=True, exist_ok=True)
    GITHUB_TOKEN = config.get('GITHUB_TOKEN', "")
    logger.info(f"GitHub Home: {GITHUB_HOME}")
    REPO_LIST = config.get('REPO_LIST', [])
    if not REPO_LIST:
        logger.error("No Repositories Found in Config File")
        return

def process_repo(repo_url: str, logger: logging.Logger):
    logger.info(f"Current Pulling [{get_repo_name_from_url(repo_url)}]")

    repo_path = ensure_repo_exists(GITHUB_HOME, repo_url, logger)
    if not repo_path:
        return

    pull_success = git_pull(repo_path, logger)
    if not pull_success:
        logger.warning(f"Regular Pull Failed, Attempting Force Pull for {repo_path.name}")
        git_pull_force(repo_path, logger)

    show_commits(repo_path, SHOW_COMMITS, logger)
    show_actions(repo_path, GITHUB_TOKEN, SHOW_ACTIONS, logger)
    logger.info(f"Finished to Pull [{repo_path.name}]")

def sync_repo_main(logger: logging.Logger = None):
    if logger is None:
        logger = setup_logging(LOG_FILE)
    start_progress(logger)
    for i,repo_url in enumerate(REPO_LIST, 1):
        logger.info(f"Processing Repository [{i} / {len(REPO_LIST)}]: {repo_url}")
        process_repo(repo_url, logger)

    logger.info("All repositories processed successfully")

if __name__ == "__main__":
    sync_repo_main()
