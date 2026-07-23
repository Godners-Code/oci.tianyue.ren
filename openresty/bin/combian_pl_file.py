#!/usr/bin/env python3
import logging
from pathlib import Path

from combian_pl_front import make_front, load_source

def load_filenames(repo_path: Path, folders: list, logger: logging.Logger) -> list:
    file_list = []
    for folder in folders:
        file_path = repo_path / folder
        if not file_path.exists():
            logger.warning(f"File Folder NOT Exists: {file_path}")
            continue
        for file_name in file_path.iterdir():
            if not file_name.name in file_list:
                file_list.append(file_name.name)
    return file_list

def make_comb_list(repo_path: Path, folders: list, file_name: str, logger: logging.Logger) -> list:
    comb_list = []
    for folder in folders:
        file_path = repo_path / folder / file_name
        file_disp = f"{folder}/{file_name}"
        if not file_path.exists():
            logger.warning(f"File Folder NOT Exists: {file_path}")
            continue
        comb_list.append(file_disp)
    logger.info(f"Found {len(comb_list)} Files for {file_name}")
    return comb_list

TABLE_HEADER = "| Item | Content |\n|:----:|:-----|\n"
def make_table(repo_path: Path, comb_list: list, logger: logging.Logger) -> str:
    table_body =[]; fm_group = []
    
    for comb_file in comb_list:
        file_path = repo_path / comb_file
        if not file_path.exists():
            logger.warning(f"File Folder NOT Exists: {file_path}")
            continue
        fm, *_ = load_source(file_path)    
        fm_group.append(fm)
    serial_names = []; updates = []
    for fm in fm_group:
        serial_names.append(fm.get('serial_title'))
        updates.append(fm.get('updated'))
    table_body.append(f"| Title | {list(set(serial_names))[0]} |")
    for fm in fm_group:
        generater = fm.get('generater')
        short_title = fm.get('short_title')
        table_body.append(f"| {generater} | {short_title} |")
    table_body.append(f"| Updated | {max(updates).strftime('%Y-%m-%d')} |")
    return f"{TABLE_HEADER}{'\n'.join(table_body)}\n\n"

def body_combian(repo_path: Path, comb_list: list, logger: logging.Logger) -> list:
    all_body = []
    for comb_file in comb_list:
        file_path = repo_path / comb_file
        if not file_path.exists():
            logger.warning(f"File Folder NOT Exists: {file_path}")
            continue
        *_, body = load_source(file_path)
        all_body.append(body)
    return all_body

def process_file_combian(repo_path: Path, comb_path: Path, folders: list, logger: logging.Logger):
    file_list = load_filenames(repo_path, folders, logger)
    for f in file_list:
        comb_list = make_comb_list(repo_path, folders, f, logger)
        front_yaml = make_front(repo_path, comb_list, logger)
        table_md = make_table(repo_path, comb_list, logger)
        all_body = body_combian(repo_path, comb_list, logger)
        full_content = front_yaml + table_md + "\n".join(all_body)

        target_path = comb_path / f"FileCombian_{f}"
        open(target_path, 'w', encoding='utf-8').write(full_content)

        logger.info(f"Successfully Merge {len(folders)} Files Into {target_path}")
