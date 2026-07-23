#!/usr/bin/env python3
import zipfile, shutil, logging, tarfile
from pathlib import Path

def extract_artifact(artifact_path: str, save_dir: str, logger: logging.Logger):
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    for item in save_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
    
    zip_extract_dir = save_dir / "_temp_zip"
    zip_extract_dir.mkdir(exist_ok=True)
    zipfile.ZipFile(artifact_path, 'r').extractall(zip_extract_dir)

    tar_files = list(zip_extract_dir.glob("*.tar"))
    if len(tar_files) != 0:
        tar_path = tar_files[0]
        tarfile.open(tar_path, 'r').extractall(save_dir)
        logger.info(f"Extracted Inner TAR File: {tar_path.name}")
    else:
        for item in zip_extract_dir.iterdir():
            shutil.move(str(item), str(save_dir / item.name))
        logger.info("No TAR File Found, Moved ZIP Contents Directly")

    shutil.rmtree(zip_extract_dir)
    Path(artifact_path).unlink(missing_ok=True)
    logger.info(f"Extracted Artifact to {save_dir}")

