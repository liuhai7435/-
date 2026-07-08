"""配置管理 - 支持 JSON 配置文件与环境变量覆盖"""

import json
import os
from pathlib import Path
from typing import Any, Optional

from .file import read_json


class Config:
    """配置管理器：从 JSON 文件加载，支持环境变量覆盖"""

    def __init__(self, config_path: str = "config.json"):
        self._config_path = Path(config_path)
        self._data: dict[str, Any] = {}
        if self._config_path.exists():
            self._data = read_json(str(self._config_path)) or {}

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项，环境变量优先（自动转大写并替换点为下划线）"""
        env_key = key.upper().replace(".", "_")
        env_val = os.environ.get(env_key)
        if env_val is not None:
            return self._cast_type(env_val)
        return self._nested_get(key, default)

    def set(self, key: str, value: Any) -> None:
        """设置配置项"""
        self._nested_set(key, value)

    def save(self, path: Optional[str] = None) -> None:
        """保存配置到文件"""
        target = Path(path) if path else self._config_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def all(self) -> dict[str, Any]:
        """返回全部配置"""
        return dict(self._data)

    # ─── 内部方法 ────────────────────────────────

    def _nested_get(self, key: str, default: Any) -> Any:
        keys = key.split(".")
        node = self._data
        for k in keys:
            if isinstance(node, dict) and k in node:
                node = node[k]
            else:
                return default
        return node

    def _nested_set(self, key: str, value: Any) -> None:
        keys = key.split(".")
        node = self._data
        for k in keys[:-1]:
            node = node.setdefault(k, {})
        node[keys[-1]] = value

    @staticmethod
    def _cast_type(value: str) -> Any:
        """尝试将字符串转为对应 Python 类型"""
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        return value
