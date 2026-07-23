#!/usr/bin/env python3
import logging
from pathlib import Path

def load_repos(repo_list_path: str, logger: logging.Logger) -> list[str]:
    path = Path(repo_list_path)
    if not path.exists():
        logger.error(f"Repository List File NOT Exists: {path}")
        return []

    repos = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                repos.append(line)
    logger.info(f"Loaded {len(repos)} Repositories URLs")
    return repos

def get_repo_name_from_url(url: str) -> str:
    if url.endswith('.git'):
        url = url[:-4]
    return url.rstrip('/').split('/')[-1]    

