#!/usr/bin/env python3
import os, logging
from pathlib import Path

from setup_logging import setup_logging
from load_config import load_config
from combian_pl_no import process_no_combian
from combian_pl_util import ensure_dirs, path_from_user
from combian_pl_spec import process_spec_combian
from combian_pl_file import process_file_combian
from combian_pl_allinone import process_allinone_combian
from combian_pl_zip import zip_grouped_files, zip_source_files, zip_allinone_file
from combian_pl_html import make_index_pl

CONF_FILE = os.path.expanduser("~/etc/combian_pl.toml")
LOG_FILE = Path("/var/log/openresty/combian_pl.log")

REPO_PATH = ""; COMB_PATH = ""; SPEC_COMBIAN = {}; NO_COMBIAN = {}; FILE_COMBIAN = []
def start_progress(config: dict, logger: logging.Logger):
    global REPO_PATH, COMB_PATH, SPEC_COMBIAN, NO_COMBIAN, FILE_COMBIAN
    REPO_PATH = path_from_user(config.get("repo_path"))
    COMB_PATH = path_from_user(config.get("comb_path"))
    SPEC_COMBIAN = config.get("spec_combian", {})
    NO_COMBIAN = config.get("no_combian", {})
    FILE_COMBIAN = config.get("combian_by_filename", [])
    ensure_dirs(COMB_PATH, logger)


def combian_pl_main(logger: logging.Logger = None):
    if logger is None:
        logger = setup_logging(LOG_FILE)
    config = load_config(CONF_FILE, logger)
    start_progress(config, logger)
    process_no_combian(REPO_PATH, COMB_PATH, NO_COMBIAN, logger)
    process_spec_combian(REPO_PATH, COMB_PATH, SPEC_COMBIAN, logger)
    process_file_combian(REPO_PATH, COMB_PATH, FILE_COMBIAN, logger)
    process_allinone_combian(REPO_PATH, COMB_PATH, logger)

    zip_grouped_files(COMB_PATH, "GroupCombian.zip", logger)
    zip_source_files(REPO_PATH, COMB_PATH, "SourcePackage.zip", logger)
    zip_allinone_file(COMB_PATH, "AllInOne.zip", logger)

    make_index_pl(COMB_PATH, logger)

if __name__ == "__main__":
    combian_pl_main()

