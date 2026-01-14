"""
日期工具
"""
from datetime import datetime, timedelta

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
            continue
    
    return None

def days_between(d1, d2):
    """计算两个日期间隔天数"""
    if isinstance(d1, str):
        d1 = parse_date(d1)
    if isinstance(d2, str):
        d2 = parse_date(d2)
    
    if d1 and d2:
        return abs((d2.date() - d1.date()).days)
    return 0

def get_date_range(commits):
    """获取提交日期范围"""
    if not commits:
        return None, None
    
    dates = [parse_date(c['date']) for c in commits if parse_date(c['date'])]
    if not dates:
        return None, None
    
    return min(dates), max(dates)
