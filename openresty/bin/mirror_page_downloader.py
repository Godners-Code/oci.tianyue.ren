#!/usr/bin/env python3
import requests, tempfile, logging
from pathlib import Path
from urllib.parse import urlparse

def get_repo_owner_name(repo_url):
    parsed = urlparse(repo_url)
    path = parsed.path.strip("/")
    if path.endswith('.git'):
        path = path[:-4]
    parts = path.split("/")
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    return None, None

def download_by_run(run: dict, headers: dict, logger: logging.Logger):
    artifacts_url = run["artifacts_url"]
    art_resp = requests.get(artifacts_url, headers=headers)
    art_resp.raise_for_status()
    artifacts = art_resp.json().get("artifacts", [])
    for artifact in artifacts:
        if artifact["expired"] or artifact["size_in_bytes"] == 0:
            continue
        download_url = artifact["archive_download_url"]
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
            tmp_path = tmp.name
            art_download = requests.get(download_url, headers=headers, stream=True)
            for chunk in art_download.iter_content(chunk_size=8192):
                tmp.write(chunk)
        repo_name = run['repository']['name']
        logger.info(f"Downloaded Artifact for {repo_name} ({artifact['size_in_bytes']} Bytes): {tmp_path}")
        return tmp_path, repo_name
    return None, None

def download_artifacts_for_repo(repo_url: str, token: str, max_search: int, logger: logging.Logger):
    owner, repo = get_repo_owner_name(repo_url)
    if not owner or not repo:
        logger.error(f"Invalid Repository URL: {repo_url}")
        return None

    headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
    }
    runs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs?per_page={max_search}"
    response = requests.get(runs_url, headers=headers)
    response.raise_for_status()
    runs = response.json().get("workflow_runs", [])
    for run in runs:
        return download_by_run(run, headers, logger)

