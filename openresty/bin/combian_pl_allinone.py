#!/usr/bin/env python3
import html, logging
from pathlib import Path
from bs4 import BeautifulSoup

README_FILE = "README.md"
COMB_FILE = "AllInOne.md"

def extract_links_from_markdown(content: str, logger) -> list:
    links = []
    seen = set()
    logger.info("Starting Link Extraction from README.md Content")
    
    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        start = 0
        while True:
            idx1 = line.find('](', start)
            if idx1 == -1:
                break
            idx2 = line.find(')', idx1 + 2)
            if idx2 == -1:
                break
            link = line[idx1 + 2:idx2].strip()
            if link.startswith('./') and (link not in seen) and (not link.endswith('.jpg')):
                seen.add(link)
                links.append(link)
                logger.info(f"Found Markdown Link: {link} at Line {line_num}.")
            start = idx2 + 1

        soup = BeautifulSoup(line, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href'].strip()
            if link.startswith('./') and (link not in seen) and (not link.endswith('.jpg')):
                seen.add(link)
                links.append(link)
                logger.info(f"Found HTML Link: {link} at Line {line_num}.")

    logger.info(f"Extraction Completed. Total Unique Links Found: {len(links)}.")
    return links

def normalize_path(base_dir: Path, relative_link: str) -> Path:
    if relative_link.startswith('./'):
        relative_link = relative_link[2:]
    return (base_dir / relative_link).resolve()

def read_file_content(file_path: Path, logger: logging.Logger) -> str:
    try:
        if not file_path.exists():
            logger.warning(f"File NOT Found: {file_path}")
            return f"\n\n --- File NOT Found: {file_path.name} ---\n\n"
        content = open(file_path, 'r', encoding='utf-8').read()
        logger.info(f"Successfully Read File: {file_path}")
        return f"\n\n--- File: {file_path.name} ---\n\n{content}\n\n"
    except Exception as e:
        logger.error(f"Failed to Read {file_path}: {e}")
        return f"\n\n--- Failed to Read {file_path}: {e} ---\n\n"

def process_allinone_combian(repo_path: Path, comb_path: Path, logger: logging.Logger):
    readme_path = repo_path / README_FILE
    readme_content = open(readme_path, 'r', encoding='utf-8').read()
    logger.info("README.md Content Loaded Successfully.")

    links = extract_links_from_markdown(readme_content, logger)

    merged_content = [ f"# Combian Documents\n\n" ]
    merged_content.append(f"# ! Source Index: README.md\n\n")
    merged_content.append(readme_content)
    merged_content.append("\n\n--- README.md End ---\n\n")
    logger.info("README.md Itself Has Been Added to the Merged Document.")

    processed_files = set()
    processed_files.add("README.md")

    file_counter = 2
    for link in links:
        file_path = normalize_path(repo_path, link)
        file_str = str(file_path)
        if file_str in processed_files:
            logger.info(f"Skipping Duplicate File: {file_path.name}")
            continue

        processed_files.add(file_str)
        relative_display = link if link.startswith('./') else f"./{link}"
        content = read_file_content(file_path, logger)
        merged_content.append(f"# ! Source File {file_counter}: {relative_display}\n")
        merged_content.append(content)
        file_counter += 1

    allinone_path = comb_path / COMB_FILE
    open(allinone_path, 'w', encoding='utf-8').write(''.join(merged_content))

    logger.info(f"Merge Completed Successfully. {len(processed_files)} Unique Files Processed.")
    logger.info(f"Output Save to {allinone_path}")

