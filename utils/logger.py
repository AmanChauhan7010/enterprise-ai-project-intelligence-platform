"""
Centralized Enterprise Logging Configuration.
Adheres to PEP8 standards and robust exception tracking.
"""
import logging
import sys
from typing import Optional


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Retrieves or initializes a configured singleton logger instance.
    
    Args:
        name (str): Name of the logger module.
        level (int): Logging severity threshold.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | [%(name)s] | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger
