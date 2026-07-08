"""字符串工具 - 常见字符串处理函数"""

import re
import random
import string as _string


def to_snake(s: str) -> str:
    """驼峰转蛇形：helloWorld -> hello_world"""
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    return s.lower()


def to_camel(s: str) -> str:
    """蛇形转驼峰：hello_world -> helloWorld"""
    parts = s.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


def truncate(s: str, max_len: int, suffix: str = "...") -> str:
    """截断字符串，超出长度加后缀"""
    if len(s) <= max_len:
        return s
    return s[:max_len - len(suffix)] + suffix


def random_str(length: int = 8) -> str:
    """生成随机字符串（字母+数字）"""
    return "".join(random.choices(_string.ascii_letters + _string.digits, k=length))


def mask_sensitive(s: str, show_start: int = 3, show_end: int = 4, mask: str = "****") -> str:
    """脱敏：保留开头和结尾，中间替换为 mask"""
    if len(s) <= show_start + show_end:
        return mask
    return s[:show_start] + mask + s[-show_end:]


def slugify(s: str, sep: str = "-") -> str:
    """将中文/特殊字符转为拼音风格的 URL slug（保留字母数字和分隔符）"""
    s = s.strip().lower()
    s = re.sub(r"[^\w\u4e00-\u9fff]+", sep, s)
    return s.strip(sep)


def is_chinese(s: str) -> bool:
    """判断字符串是否包含中文"""
    return bool(re.search(r"[\u4e00-\u9fff]", s))
