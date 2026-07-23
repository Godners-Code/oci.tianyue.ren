#!/usr/bin/env python3
import os, git
from git import GitCommandError
from gh_backup_url import prepare_auth_url

def push_to_destination(repo, dest, logger):
    git_url = dest['git_url']
    auth_type = dest.get('auth_type', 'none')
    auth_value = dest.get('auth_value')

    push_url = prepare_auth_url(git_url, auth_type, auth_value)

    dest_name = dest.get('name', 'unknown')

    logger.info(f"Start to Clone to {dest_name} Push {git_url} Forcely")

    env = os.environ.copy()
    if auth_type == 'ssh' and auth_value:
        key_path = os.path.expanduser(f"~/etc/{auth_value}")
        env['GIT_SSH_COMMAND'] = f"ssh -i {key_path} -o StrictHostKeyChecking=no IdentitiesOnly=yes"
        logger.info(f"Using SSH Key: {key_path}")


    try:
        remote_name = f"dest_{dest_name}"
        if remote_name in repo.remotes:
            repo.delete_remote(remote_name)
        remote = repo.create_remote(remote_name, push_url)

        branch = repo.active_branch.name
        logger.info(f"Current Branch: {branch}")

        push_info = remote.push(refspec=f"{branch}:{branch}", force=True, env=env)
        remote.push(refspec="refs/tags/*:refs/tags/*", force=True, env=env)

        for info in push_info:
            if info.flags & git.PushInfo.ERROR:
                logger.error(f"Pushing Failed: {info.summary}")
            else:
                logger.info(f"Pushing Successfully: {info.summary}")

        logger.info(f"Pushing {dest_name} Finished.")
    except GitCommandError as e:
        logger.error(f"Pushing Failed {dest_name}: {e}")
        raise
    except Exception as e:
        logger.error(f"Pushing Abnormal {dest_name}: {e}")
        raise

