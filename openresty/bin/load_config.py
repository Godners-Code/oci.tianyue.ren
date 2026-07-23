#!/usr/bin/env python3
import os, logging, tomllib
from pathlib import Path

def load_config(conf_path: str, logger: logging.Logger) -> dict:
    toml_path = Path(conf_path)
    if not toml_path.exists():
        logger.error(f"Config File NOT Exist: {conf_path}")
        raise FileNotFoundError(f"Config File NOT Exist: {conf_path}")
    config = tomllib.load(open(toml_path, 'rb'))
    logger.info(f"Loaded Configuration from {conf_path}")
    return config

