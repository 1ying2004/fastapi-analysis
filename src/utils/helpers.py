"""
辅助函数模块

提供通用的辅助函数。
"""
from datetime import datetime


def format_number(n):
    """格式化数字，添加千位分隔符"""
    return f"{n:,}"


def format_date(dt):
    """格式化日期为字符串"""
    if isinstance(dt, str):
        return dt
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def truncate_str(s, max_len=50):
    """截断字符串"""
    if len(s) <= max_len:
        return s
    return s[:max_len-3] + '...'


def safe_divide(a, b):
    """安全除法，避免除零错误"""
    if b == 0:
        return 0
    return a / b


def parse_date(date_str):
    """解析日期字符串"""
    formats = [
        '%Y-%m-%d %H:%M:%S %z',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%d',
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            pass
    return None
