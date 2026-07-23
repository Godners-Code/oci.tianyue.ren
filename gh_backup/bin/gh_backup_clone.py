#!/usr/bin/env python3
import os, git
from git import GitCommandError
from gh_backup_name import get_repo_name_from_url
from gh_backup_url import prepare_auth_url

def clone_repository(source, temp_dir, logger):
    git_url = source['git_url']
    auth_type = source.get('auth_type', 'none')
    auth_value = source.get('auth_value')

    clone_url = prepare_auth_url(git_url, auth_type, auth_value)
    repo_name = get_repo_name_from_url(git_url)
    clone_path = os.path.join(temp_dir, repo_name)

    logger.info(f"Start to Clone Repository {git_url} -> {clone_url}")

    env = os.environ.copy()
    if auth_type == 'ssh' and auth_value:
        env['GIT_SSH_COMMAND'] = f"ssh -i {auth_value} -o StrictHostKeyChecking=no"

    try:
        repo = git.Repo.clone_from(
                clone_url,
                clone_path,
                env=env if auth_type == 'ssh' else None,
                multi_options=['--no-single-branch', '--tags', '--progress']
        )
        logger.info(f"Cloning Finished: {repo_name}")
        return repo, clone_path
    except GitCommandError as e:
        logger.error(f"Cloning Failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Cloning Abnormal: {e}")
        raise

