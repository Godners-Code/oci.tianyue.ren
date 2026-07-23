#!/usr/bin/env python3
import sys, logging
from pathlib import Path

def get_file_list(comb_path: Path, logger: logging.Logger) -> list:
    file_names = []
    for file_path in comb_path.iterdir():
        if file_path.is_file() and file_path.name != "index.html":
            file_names.append(file_path.name)
    logger.info(f"Found {len(file_names)} Files in {comb_path}")
    return sorted(file_names)

def make_html_code(file_name: str) -> str:
    if file_name.endswith('.zip'):
        file_disp = f"[{file_name}]"
    else:
        file_disp = file_name
    return f'<a href="./{file_name}" download="{file_name}">{file_disp}</a><br />'


def write_html_file(comb_path: Path, file_names: list, logger: logging.Logger) -> None:
    htmls = []
    for file_name in file_names:
        htmls.append(make_html_code(file_name))
    try:
        index_file = comb_path / "index.html"
        open(index_file, 'w', encoding='utf-8').write('\n'.join(htmls))
        logger.info(f"Successfully Writen {index_file}, Processed {len(file_names)} Files.")
    except Exception as e:
        logger.error(f"Write HTML Failed: {e}")

def make_index_pl(comb_path: Path, logger: logging.Logger) -> None:
    logger.info("Start to Process index.html")
    file_names = get_file_list(comb_path, logger)
    write_html_file(comb_path, file_names, logger)

