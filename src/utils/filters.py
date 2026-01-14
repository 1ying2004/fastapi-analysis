"""
数据过滤器
"""
from datetime import datetime

def filter_by_author(commits, author):
    """按作者过滤"""
    return [c for c in commits if c['author'] == author]

def filter_by_date_range(commits, start_date, end_date):
    """按日期范围过滤"""
    result = []
    for c in commits:
        try:
            date = datetime.fromisoformat(c['date'].replace('Z', '+00:00'))
            if start_date <= date <= end_date:
                result.append(c)
        except:
            pass
    return result

def filter_by_message(commits, keyword):
    """按关键词过滤"""
    keyword = keyword.lower()
    return [c for c in commits if keyword in c['message'].lower()]

def filter_by_type(commits, commit_type):
    """按类型过滤"""
    return [c for c in commits if c['message'].lower().startswith(commit_type)]
