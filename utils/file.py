"""文件工具 - 常用文件操作封装"""

import json
import re
from pathlib import Path
from typing import Any, Optional


def ensure_dir(path: str) -> Path:
    """确保目录存在，返回 Path 对象"""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def read_json(path: str) -> Optional[dict]:
    """读取 JSON 文件"""
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def write_json(path: str, data: Any, indent: int = 2) -> None:
    """写入 JSON 文件，自动创建父目录"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(data, ensure_ascii=False, indent=indent),
        encoding="utf-8",
    )


def safe_filename(name: str) -> str:
    """将字符串转为安全的文件名（移除非法字符）"""
    return re.sub(r"[<>:\"/\\|?*]", "_", name)


def get_file_size(path: str) -> str:
    """获取文件大小的可读表示"""
    p = Path(path)
    if not p.exists():
        return "0 B"
    size = p.stat().st_size
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def list_files(directory: str, pattern: str = "*", recursive: bool = False) -> list[Path]:
    """列出目录下匹配的文件"""
    p = Path(directory)
    if not p.exists():
        return []
    if recursive:
        return list(p.rglob(pattern))
    return list(p.glob(pattern))
