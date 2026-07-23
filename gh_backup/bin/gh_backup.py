#!/usr/bin/env python3
import os, sys, yaml, tempfile, shutil, fcntl, time, git
from pathlib import Path
from datetime import datetime
from git import GitCommandError

from gh_backup_log import setup_logging
from gh_backup_clone import clone_repository
from gh_backup_push import push_to_destination
from gh_backup_name import get_repo_name_from_url
from gh_backup_check import validate_config

def acquire_lock(lock_file):
    try:
        lock_fd = open(lock_file, 'w')
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_fd
    except BlockingIOError:
        return None

def process_config(config_path, temp_base, logger):
    try:
        config = yaml.safe_load(open(config_path, 'r', encoding='utf-8'))
        if not validate_config(config, config_path, logger): return

        source_list = config.get('source')
        destinations = config.get('destination')

        logger.info(f"Processed Configuration File: {config_path}")

        source = source_list[0]
        repo_name = get_repo_name_from_url(source['git_url'])
        temp_dir = os.path.join(temp_base, f"{repo_name}_{int(time.time())}")
        os.makedirs(temp_dir, exist_ok=True)

        repo, clone_path = clone_repository(source, temp_dir, logger)

        for dest in destinations:
            push_to_destination(repo, dest, logger)

        repo.close()
        shutil.rmtree(clone_path, ignore_errors=True)
        logger.info(f"Process {repo_name} Finished, Temporary Files Cleaned Up.")

    except Exception as e:
        logger.error(f"Process Configuration {config_path} Failed: {e}")

def main():
    home = os.path.expanduser("~")
    config_dir = os.path.join(home, "etc")
    script_name = os.path.basename(__file__)
    lock_file = os.path.join(tempfile.gettempdir(), f"{script_name}.lock")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = "/var/log/gh_backup"
    log_file = os.path.join(log_dir, f"gh_backup.{timestamp}.log")

    logger = setup_logging(log_file)

    lock_fd = acquire_lock(lock_file)
    if not lock_fd:
        logger.warning("Another Instance is Running, Exit.")
        print("Another Instance is Running, Exit.")
        sys.exit(1)

    try:
        if not os.path.exists(config_dir):
            logger.error(f"Configure Folder does NOT Exist: {config_dir}")
            sys.exit(1)

        config_files = sorted(Path(config_dir).glob("*_backup.yml"))
        if not config_files:
            logger.info(f"No Configure File (*_backup.yml) in {config_dir}.")
            sys.exit(0)

        logger.info(f"Found {len(config_files)} Configure Files.")

        with tempfile.TemporaryDirectory(prefix="gh_backup_") as temp_base:
            for config_path in config_files:
                process_config(str(config_path), temp_base, logger)

        logger.info("All Backup Tasks Finished.")

    except Exception as e:
        logger.error(f"Main Progress Abnormal: {e}")
    finally:
        if lock_fd:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()
            try:
                os.unlink(lock_file)
            except:
                pass

if __name__ == "__main__":
    main()
                       
