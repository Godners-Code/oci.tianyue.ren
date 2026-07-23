#!/usr/bin/env python3
import os, sys, logging
from datetime import datetime

def setup_logging(log_file):
    logger = logging.getLogger(os.environ.get('USER'))
    logger.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    return logger

def double_logging(log_file: str, log_show: str) -> logging.Logger:
    logger = logging.getLogger('openresty')
    logger.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    with open(log_show, 'w', encoding='utf-8') as f:
        pass
    show_handler = logging.FileHandler(log_show, encoding='utf-8')
    show_handler.setLevel(logging.INFO)
    show_handler.setFormatter(log_formatter)
    logger.addHandler(show_handler)

    return logger


