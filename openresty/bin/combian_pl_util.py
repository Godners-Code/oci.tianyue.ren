#!/usr/bin/env python3
import logging, os, frontmatter, re
from pathlib import Path

def ensure_dirs(comb_path: Path, logger: logging.Logger):
    comb_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Checked Combian Path Exists: {comb_path}")

def path_from_user(rel_path: str) -> Path:
    return Path(os.path.expanduser(rel_path))

def match_heading(body: str) -> str:
    heading_match = re.search(r'^(#\s+.+?)$', body, re.MULTILINE)
    return heading_match.group(1).strip() if heading_match else "No TItle"

