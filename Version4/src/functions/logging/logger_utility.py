import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(
    logger_name: str,
    log_file: str,
    level: int = logging.INFO,
    max_bytes: int = 5 * 1024 * 1024,  # 5 MB
    backup_count: int = 3,
    console_output: bool = True
) -> logging.Logger:
    """
    Configures and returns a logger.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

    # Console handler (optional)
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(console_handler)

    logger.info(f"Logger {logger_name} initialized with file {log_file}")
    return logger
