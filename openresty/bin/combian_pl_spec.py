#!/usr/bin/env python3
import logging
from pathlib import Path
from datetime import date

from combian_pl_front import make_front, load_source
from combian_pl_util import match_heading

def table_line(front: dict, source_name: str) -> str:
    line_str  = f"| {front.get('title', 'None')} | "
    line_str += f"{front.get('serial_title', 'None')} | "
    line_str += f"{front.get('short_title', 'None')} | "
    line_str += f"{front.get('updated', date(2020, 1, 1)).strftime('%Y-%m-%d')} | "
    line_str += f"{source_name} |"
    return line_str

TABLE_HEADER = "| Title | Serial Title | Short Title | Updated | Source |\n|:-----:|:------------:|:-----------:|:-------:|:-------|\n"

def make_table(repo_path: Path, source_list: list, logger: logging.Logger) -> str:
    table_body = []
    for src in source_list:
        source_path = repo_path / src
        if not source_path.exists():
            logger.warning("Source File NOT Found: {src_path}")
            continue
        fm, *_ = load_source(source_path)
        table_body.append(table_line(fm, src))
    return f"{TABLE_HEADER}{'\n'.join(table_body)}\n\n"

def body_combian(repo_path: Path, source_list: list, logger: logging.Logger) -> list:
    all_body = []
    for src in source_list:
        source_path = repo_path / src
        if not source_path.exists():
            logger.warning("Source File NOT Found: {src_path}")
            continue
        *_, body = load_source(source_path)
        all_body.append(body)
    return all_body

def process_spec_combian(repo_path: Path, comb_path: Path, config: list, logger: logging.Logger):
    for conf in config:
        source_list = conf.get("source_list")
        front_yaml = make_front(repo_path, source_list, logger)
        table_md = make_table(repo_path, source_list, logger)
        all_body = body_combian(repo_path, source_list, logger)
        full_content = front_yaml + table_md + "\n".join(all_body)

        target_path = comb_path / conf.get("target_name")
        open(target_path, 'w', encoding='utf-8').write(full_content)

        logger.info(f"Successfully Merge {len(source_list)} Files Into {target_path}")

