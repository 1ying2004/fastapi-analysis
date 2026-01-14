"""
统计分析模块

提供对Git提交数据的统计分析功能，
包括作者贡献、时间分布、消息类型等。
"""
from collections import Counter
from datetime import datetime
import pandas as pd


def get_author_stats(commits):
    """
    统计作者贡献数量
    
    Args:
        commits: 提交记录列表
    
    Returns:
        作者贡献统计字典，按贡献数降序排列
    """
    authors = Counter(c['author'] for c in commits)
    return dict(authors.most_common())


def get_time_distribution(commits):
    """
    统计提交时间分布
    
    分析提交在年、月、星期、小时维度的分布情况
    
    Args:
        commits: 提交记录列表
    
    Returns:
        包含by_year, by_month, by_weekday, by_hour的字典
    """
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
    """
    统计提交消息类型
    
    按conventional commits规范分类统计
    """
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
    """
    生成完整统计报告
    
    Args:
        commits: 提交记录列表
    
    Returns:
        包含所有统计信息的字典
    """
    return {
        'total_commits': len(commits),
        'unique_authors': len(set(c['author'] for c in commits)),
        'author_stats': get_author_stats(commits),
        'time_distribution': get_time_distribution(commits),
        'message_types': get_message_stats(commits)
    }
