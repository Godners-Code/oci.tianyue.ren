#!/usr/bin/env python3
from pathlib import Path

def ensure_dirs(config):
    Path(config['PAGES_HOME']).expanduser().mkdir(parents=True, exist_ok=True)
    Path("~/etc").expanduser().mkdir(parents=True, exist_ok=True)
    Path("~/bin").expanduser().mkdir(parents=True, exist_ok=True)

def cleanup_temp(temp_path):
    if Path(temp_path).exists():
        Path(temp_path).unlink(missing_ok=True)
