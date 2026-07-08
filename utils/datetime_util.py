"""日期时间工具 - 常用日期格式化与计算"""

from datetime import datetime, timezone, timedelta
from typing import Optional


def now(tz: Optional[timezone] = None) -> datetime:
    """返回当前时间"""
    return datetime.now(tz=tz)


def today() -> str:
    """返回今天的日期字符串 yyyy-mm-dd"""
    return datetime.now().strftime("%Y-%m-%d")


def format_dt(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化 datetime 为字符串"""
    return dt.strftime(fmt)


def parse_dt(s: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """从字符串解析 datetime，失败返回 None"""
    try:
        return datetime.strptime(s, fmt)
    except (ValueError, TypeError):
        return None


def time_ago(dt: datetime) -> str:
    """返回 '刚刚 / x分钟前 / x小时前 / x天前' 风格的时间描述"""
    diff = datetime.now() - dt
    seconds = diff.total_seconds()

    if seconds < 60:
        return "刚刚"
    minutes = int(seconds // 60)
    if minutes < 60:
        return f"{minutes}分钟前"
    hours = minutes // 60
    if hours < 24:
        return f"{hours}小时前"
    days = hours // 24
    if days < 30:
        return f"{days}天前"
    return dt.strftime("%Y-%m-%d")


def timestamp() -> int:
    """返回当前 Unix 时间戳（秒）"""
    return int(datetime.now().timestamp())


def iso_format(dt: datetime) -> str:
    """返回 ISO 8601 格式字符串"""
    return dt.isoformat()
