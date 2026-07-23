#!/usr/bin/env python3
import logging, git
from pathlib import Path

from sync_repo_loader import get_repo_name_from_url

def ensure_repo_exists(github_home: Path, repo_url: str, logger: logging.Logger):
    repo_name = get_repo_name_from_url(repo_url)
    repo_path = github_home / repo_name

    if repo_path.exists():
        logger.info(f"Repository Already Exists: {repo_name}")
        return repo_path

    logger.info(f"Cloning Repository: {repo_url}")
    try:
        git.Repo.clone_from(repo_url, str(repo_path))
        logger.info(f"Git Clone Successful: {repo_name}")
        return repo_path
    except Exception as e:
        logger.error(f"Clone Failed {repo_url}: {e}")
        return None

def git_pull(repo_path: Path, logger: logging.Logger) -> bool:
    logger.info(f"Pulling Repository: {repo_path.name}")
    try:
        repo = git.Repo(str(repo_path))
        origin = repo.remotes.origin
        origin.pull()
        logger.info(f"Git Pull Completed: {repo_path.name}")
        return True
    except Exception as e:
        logger.error(f"Pull Failed {repo_path.name}: {e}")
        return False

def git_pull_force(repo_path: Path, logger: logging.Logger) -> bool:
    logger.info(f"Force Pulling Repository: {repo_path.name}")
    try:
        repo = git.Repo(str(repo_path))
        repo.git.fetch('--all')
        repo.git.reset('--hard', 'origin/main')
        repo.git.clean('-fd')
        logger.info(f"Git Force Pull Completed: {repo_path.name}")
        return True
    except Exception as e:
        logger.error(f"Force Pull Failed {repo_path.name}: {e}")
        return False
