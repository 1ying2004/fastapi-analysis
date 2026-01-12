"""
格式化工具
"""
from datetime import datetime

def format_date(dt, fmt='%Y-%m-%d'):
    """格式化日期"""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except:
            return dt
    return dt.strftime(fmt)

def format_number(n):
    """格式化数字（加千分位）"""
    return f'{n:,}'

def truncate(s, length=50):
    """截断字符串"""
    if len(s) <= length:
        return s
    return s[:length-3] + '...'

def safe_divide(a, b):
    """安全除法"""
    return a / b if b != 0 else 0

def percentage(part, total):
    """计算百分比"""
    return safe_divide(part * 100, total)
