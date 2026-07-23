#!/usr/bin/env python3
import logging, sys
from pathlib import Path

def load_urls(list_path: str, logger: logging.Logger) -> list[str]:
    path = Path(list_path)
    if not path.exists():
        logger.error(f"LIst File does NOT EXIST: {list_path}")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        return urls

    
