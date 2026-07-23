#!/usr/bin/env python3
import shutil, logging
from pathlib import Path

def copy_no_combian(config: dict, logger: logging.Logger):
    source_path = config.get("source_path")
    target_path = config.get("target_path")
    if not source_path:
        logger.warning(f"WITHOUT Combian File NOT Exist: {source_path}")
        return
    shutil.copy2(source_path, target_path)
    logger.info(f"Copied {source_path.name} to {target_path}")

def process_no_combian(repo_path: Path, comb_path: Path, config: dict, logger: logging.Logger):
    logger.info(f"Loaded {len(config)} Files WITHOUT Combian.")
    for conf in config:
        conf["source_path"] = repo_path / conf.get("source_name", "")
        conf["target_path"] = comb_path / conf.get("target_name", "")
        copy_no_combian(conf, logger)

