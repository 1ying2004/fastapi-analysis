"""
统计分析模块
"""
from collections import Counter
from datetime import datetime
import pandas as pd

def get_author_stats(commits):
    """统计作者贡献"""
    authors = Counter(c['author'] for c in commits)
    return dict(authors.most_common())

def get_time_distribution(commits):
    """统计时间分布"""
    df = pd.DataFrame(commits)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    
    return {
        'by_year': df.groupby(df['date'].dt.year).size().to_dict(),
        'by_month': df.groupby(df['date'].dt.month).size().to_dict(),
        'by_weekday': df.groupby(df['date'].dt.dayofweek).size().to_dict(),
        'by_hour': df.groupby(df['date'].dt.hour).size().to_dict()
    }

def get_message_stats(commits):
    """统计消息类型"""
    types = {'feat': 0, 'fix': 0, 'docs': 0, 'refactor': 0, 'test': 0, 'other': 0}
    
    for c in commits:
        msg = c['message'].lower()
        found = False
        for t in types:
            if msg.startswith(t):
                types[t] += 1
                found = True
                break
        if not found:
            types['other'] += 1
    
    return types

def generate_report(commits):
    """生成统计报告"""
    return {
        'total_commits': len(commits),
        'unique_authors': len(set(c['author'] for c in commits)),
        'author_stats': get_author_stats(commits),
        'time_distribution': get_time_distribution(commits),
        'message_types': get_message_stats(commits)
    }
