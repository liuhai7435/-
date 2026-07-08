"""数据验证工具 - 常见格式校验"""

import re
from typing import Any, Callable, Optional


# ─── 独立验证函数 ────────────────────────────

def is_email(value: str) -> bool:
    """校验邮箱格式"""
    if not value:
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, value))


def is_phone(value: str) -> bool:
    """校验中国大陆手机号"""
    if not value:
        return False
    return bool(re.match(r"^1[3-9]\d{9}$", value))


def is_url(value: str) -> bool:
    """校验 URL 格式"""
    if not value:
        return False
    pattern = r"^https?://[^\s/$.?#].[^\s]*$"
    return bool(re.match(pattern, value))


def is_number(value: Any) -> bool:
    """判断是否为数字（支持字符串数字）"""
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False
    return False


def not_empty(value: Any) -> bool:
    """判断值是否非空（None、空字符串、空列表等均视为空）"""
    if value is None:
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    if hasattr(value, "__len__") and len(value) == 0:
        return False
    return True


def in_range(value: int | float, min_val: int | float, max_val: int | float) -> bool:
    """判断数值是否在闭区间内"""
    return min_val <= value <= max_val


# ─── 链式验证器 ──────────────────────────────

class Validator:
    """链式数据验证器，支持自定义规则"""

    def __init__(self, value: Any, field: str = "字段"):
        self.value = value
        self.field = field
        self._errors: list[str] = []

    def required(self, message: str = "") -> "Validator":
        """必填校验"""
        if not not_empty(self.value):
            self._errors.append(message or f"{self.field}不能为空")
        return self

    def min_len(self, length: int, message: str = "") -> "Validator":
        """最小长度"""
        if self.value is not None and len(str(self.value)) < length:
            self._errors.append(message or f"{self.field}长度不能少于{length}")
        return self

    def max_len(self, length: int, message: str = "") -> "Validator":
        """最大长度"""
        if self.value is not None and len(str(self.value)) > length:
            self._errors.append(message or f"{self.field}长度不能超过{length}")
        return self

    def email(self, message: str = "") -> "Validator":
        """邮箱格式"""
        if self.value and not is_email(str(self.value)):
            self._errors.append(message or f"{self.field}格式不正确")
        return self

    def phone(self, message: str = "") -> "Validator":
        """手机号格式"""
        if self.value and not is_phone(str(self.value)):
            self._errors.append(message or f"{self.field}格式不正确")
        return self

    def custom(self, fn: Callable[[Any], bool], message: str = "") -> "Validator":
        """自定义校验函数"""
        if self.value is not None and not fn(self.value):
            self._errors.append(message or f"{self.field}校验不通过")
        return self

    def ok(self) -> bool:
        """校验是否通过"""
        return len(self._errors) == 0

    def errors(self) -> list[str]:
        """获取所有错误信息"""
        return list(self._errors)

    def first_error(self) -> Optional[str]:
        """获取第一个错误"""
        return self._errors[0] if self._errors else None

    def raise_if_error(self):
        """校验不通过时抛出 ValueError"""
        if self._errors:
            raise ValueError(self._errors[0])
