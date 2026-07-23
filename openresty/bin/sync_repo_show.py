#!/usr/bin/env python3
import logging, requests, git
from datetime import datetime
from pathlib import Path

def show_commits(repo_path: Path, show_count: int, logger: logging.Logger):
    try:
        repo = git.Repo(str(repo_path))
        commits = list(repo.iter_commits(max_count=show_count))
        total = len(list(repo.iter_commits()))

        logger.info(f"Last [{show_count} of {total}] Commits for {repo_path.name}")
        print(f"\n === Last [{show_count} of {total}] Commits for {repo_path.name}")
        print("ID      DATE       TIME     MESSAGE")
        print("------- ---------- -------- -----------------")
        for commit in commits:
            dt = datetime.fromtimestamp(commit.committed_date)
            print(f"{commit.hexsha[:7]} {dt.strftime('%F %T')} {commit.summary}")
        if total > show_count:
            print("....... .......... ........ .................")
        print("")
    except Exception as e:
        logger.error(f"Failed to Show Commits: {e}")


def show_actions(repo_path: Path, token: str, show_count: int, logger: logging.Logger):
    try:
        repo = git.Repo(str(repo_path))
        remote_url = repo.remotes.origin.url
    
        if 'github.com' not in remote_url:
            return
        remote_url = remote_url.split('github.com/')[-1]
        if remote_url.endswith('.git'):
            remote_url = remote_url[:-4]
        parts = remote_url.split('/')
        owner, repo_name = parts[-2], parts[-1]
        owner = owner.replace('git@github.com:', '')

#        token = load_github_token(logger)
        headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
        }

        logger.info(f"Fetching Actions for {repo_path.name}")
        print(f"\n === Last [{show_count}] Actions for {repo_path.name}:")
        url = f"https://api.github.com/repos/{owner}/{repo_name}/actions/runs?per_page={show_count}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json().get('workflow_runs', [])

        print("ID       STATUS   EVENT    DATE       TIME     DURATION TITLE")
        print("-------- -------- -------- ---------- -------- -------- -----")
        for run in data:
            created = datetime.fromisoformat(run['created_at'].replace('Z', '+00:00'))
            title = (run.get('display_title') or '')[:24]
            print(f"{str(run.get('id', ''))[:8]:8} {run.get('status', '')[:8]:8} {run.get('event', '')[:8]:8} {created.strftime('%F %T')} N/A       {title}")
    except Exception as e:
        logger.error(f"Failed to Show Actions: {e}")
    



