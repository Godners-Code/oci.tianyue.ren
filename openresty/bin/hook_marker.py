#!/usr/bin/env python3
import logging, os
from pathlib import Path

def write_marker(marker_file: Path, logger: logging.Logger) -> int:
    pid = os.getpid()
    logger.info(f" ======== Current Process PID: {pid} ========")
    try:
        marker_file.write_text(str(pid))
        logger.info(f" ======== Written Own PID {pid} to {marker_file} ========")
        return pid
    except Exception as e:
        logger.error(f" ======== Failed to Write PID to Wait Marker: {e} ========")
        return None

def check_marker(marker_file: Path, own_pid: int, logger: logging.Logger) -> bool:
    try:
        if not marker_file.exists():
            logger.warning(" ======== Wait Marker File Disappeared.  ========")
            return False
        current_content = marker_file.read_text().strip()
        if current_content != str(own_pid):
            logger.info(f" ======== Marker PID changed to {current_content}, NOT Matching Expected {own_pid} ========")
            return False
        return True
    except Exception as e:
        logger.error(f"Error Checking Marker PID: {e}")
        return False

def remove_marker(marker_file: Path, logger: logging.Logger):
    try:
        if marker_file.exists():
            marker_file.unlink()
            logger.info(" ======== Cleaned up Wait Marker File ========")
    except Exception as e:
        logger.warning(f" ======== Fail to Clean Marker File: {e} ========")

