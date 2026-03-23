"""
Logging configuration for the application.
Provides structured logging to console and file.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging(log_level=logging.INFO):
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger("formulari_app")
    logger.setLevel(log_level)

    # Prevent duplicate handlers
    if logger.hasHandlers():
        return logger

    # Log format: [TIMESTAMP] [LEVEL] [MODULE] Message
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (rotating, max 10MB, keep 5 backups)
    log_file = os.path.join(log_dir, "formulari_app.log")
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)  # File gets more details
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("=" * 60)
    logger.info(f"Application started at {datetime.now().isoformat()}")
    logger.info("=" * 60)

    return logger

# Create a singleton logger instance
logger = setup_logging()
