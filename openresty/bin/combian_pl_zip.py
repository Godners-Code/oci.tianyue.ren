#!/usr/bin/env python3
import os, zipfile, glob, logging
from pathlib import Path


GROUP_PREFIXES = [ 'FileCombian_', 'SpecCombian_', 'Source_' ]
EXCLUDE_FOLDER = {".git", ".github"}

def find_grouped_files(comb_path: Path) -> list:
    selected_files = []
    for file_path in comb_path.iterdir():
        if not file_path.is_file():
            continue
        for prefix in GROUP_PREFIXES:
            if file_path.name.startswith(prefix):
                selected_files.append(file_path)
                break
    return selected_files

def zip_grouped_files(comb_path: Path, zip_file: str, logger: logging.Logger):
    zip_path = comb_path / zip_file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in find_grouped_files(comb_path):
            zipf.write(f, arcname=f.name)
            logger.info(f"Appended {f.name} to {zip_path.name}")

def zip_source_files(repo_path: Path, comb_path: Path, zip_file: str, logger: logging.Logger):
    zip_path = comb_path / zip_file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_FOLDER]
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(repo_path)
                zipf.write(file_path, arcname)
                logger.info(f"Appended {arcname} to {zip_path.name}")

def zip_allinone_file(comb_path: Path, zip_file: str, logger: logging.Logger):
    zip_path = comb_path / zip_file
    zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED).write(comb_path / "AllInOne.md", arcname="AllInOne.md")
    logger.info(f"Append AllInOne.md to {zip_path.name}")

