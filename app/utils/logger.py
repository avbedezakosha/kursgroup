import logging
import sys
from pathlib import Path
from typing import Optional, Union


def setup_logger(
        name: str = __name__,
        level: Union[int, str] = logging.INFO
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)8s] [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def get_child_logger(
        parent_name: str,
        child_name: str
) -> logging.Logger:
    return logging.getLogger(f"{parent_name}.{child_name}")
