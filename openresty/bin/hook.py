#!/usr/bin/env python3
import os, sys, logging, shutil, time, subprocess
from datetime import datetime
from pathlib import Path

from hook_marker import write_marker, check_marker, remove_marker
from setup_logging import double_logging
from load_config import load_config

from sync_repo import sync_repo_main
from mirror_page import mirror_page_main
from combian_pl import combian_pl_main

COLLECT_PL = os.path.expanduser("~/bin/collect-pl.sh")   # To ReBuild

LOG_FILE = Path("/var/log/openresty/hook.runtime.log")
LOG_SHOW = Path(os.path.expanduser("~/html/hook.log"))
CONF_FILE = os.path.expanduser("~/etc/hook.toml")

MARKER_FILE = ""; MIRROR_PATH_WAIT = 0; TIME_FORMAT = ""
def start_progress(conf: dict, logger: logging.Logger):
    global TIME_FORMAT, MARKER_FILE, MIRROR_PAGE_WAIT
    TIME_FORMAT = conf.get("time_format")
    MARKER_FILE = Path(conf.get("marker_file"))
    MIRROR_PAGE_WAIT = conf.get("mirror_page_wait")

def wait_mirror_page(logger: logging.Logger):
    pid = write_marker(MARKER_FILE, logger)
    if pid is None:
        logger.error(" ======== Failed to write PID, Exiting ========")
        sys.exit(1)

    for i in range(MIRROR_PAGE_WAIT, 0, -1):
        time_now = datetime.now().strftime(TIME_FORMAT)
        logger.info(f" ======== Waiting [ {time_now} Remainder {i} Minutes ] ========")
        time.sleep(60)

        if not check_marker(MARKER_FILE, pid, logger):
            logger.info(" ======== PID Check Failed Exiting Current Process ========")
            sys.exit(0)

    remove_marker(MARKER_FILE, logger)

def run_combian(logger: logging.Logger):
    combian_pl_main(logger)
    # 合并VR仓库
    # 合并TE仓库

def hook_main(logger: logging.Logger = None):
    if logger is None:
        logger = double_logging(LOG_FILE, LOG_SHOW)
    hook_start = datetime.now()
    config = load_config(CONF_FILE, logger)
    start_progress(config, logger)
    logger.info(f" ======== Hooking Started at [ {hook_start.strftime(TIME_FORMAT)} ] ========")
    sync_repo_main(logger)
    wait_mirror_page(logger)
    mirror_page_main(logger)
    run_combian(logger)
    hook_final = datetime.now()
    logger.info(f" ======== Hooking Finally at [ {hook_final.strftime(TIME_FORMAT)} ] ========")
    logger.info(f" ======== Hooking Spent Time [ {(hook_final - hook_start).total_seconds():.6f} Seconds ] ========")

if __name__ == "__main__":
    hook_main()
