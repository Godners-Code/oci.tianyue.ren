#!/usr/bin/env python3
import logging, os, frontmatter, yaml
from pathlib import Path

from combian_pl_util import match_heading

def load_source(source_file: Path):
    post = frontmatter.load(source_file)
    body = post.content.strip()
    fm = post.metadata
    heading = match_heading(body)
    return fm, heading, body

def collect_front(frontmatters: list, combian_list: list) -> dict:
    layouts = set()
    serial_titles = set()
    short_titles = set()
    for fm in frontmatters:
        if isinstance(fm, dict):
            if 'layout' in fm:
                layouts.add(str(fm['layout']))
            if 'serial_title' in fm:
                serial_titles.add(str(fm['serial_title']))
            if 'short_title' in fm:
                short_titles.add(str(fm['short_title']))
    return {
            'layout': sorted(list(layouts)),
            'serial_title': sorted(list(serial_titles)),
            'short_title': sorted(list(short_titles)),
            'combian_list': combian_list,
    }

def make_front(repo_path: Path, source_list: list, logger: logging.Logger):
    logger.info(f"Starting Merge Front Matter from {len(source_list)} Files.")
    combian_list = []; merged_content = []; frontmatters = []; headings = []
    for src in source_list:
        src_path = repo_path / src
        if not src_path.exists():
            logger.warning(f"Source File NOT Found: {src_path}")
            continue

        fm, heading, _ = load_source(src_path)
        combian_list.append(src)
        frontmatters.append(fm)
        headings.append(heading)
    new_fm = collect_front(frontmatters, combian_list)
    new_yaml = yaml.dump(new_fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    new_yaml = f"---\n{new_yaml}---\n\n"
    return new_yaml

