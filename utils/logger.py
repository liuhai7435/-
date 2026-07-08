"""日志工具 - 统一日志配置与获取"""

import logging
import sys
from pathlib import Path


def setup_logger(
    name: str = "app",
    level: int = logging.INFO,
    log_dir: str = "logs",
    fmt: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt: str = "%Y-%m-%d %H:%M:%S",
    to_console: bool = True,
    to_file: bool = True,
) -> logging.Logger:
    """配置并返回一个 logger，同时输出到控制台和文件"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()  # 避免重复添加

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    if to_console:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if to_file:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            Path(log_dir) / f"{name}.log", encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "app") -> logging.Logger:
    """获取已有 logger，不存在则返回默认 logger"""
    return logging.getLogger(name)
