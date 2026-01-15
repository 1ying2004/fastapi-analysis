"""
PR分析模块

分析Pull Requests数据
"""
from collections import Counter
from datetime import datetime
import json


def analyze_prs(prs):
    """
    分析PR数据
    
    Args:
        prs: PR列表
    
    Returns:
        分析结果字典
    """
    if not prs:
        return {}
    
    states = Counter(pr['state'] for pr in prs)
    
    authors = Counter(pr['author'] for pr in prs)
    top_authors = authors.most_common(20)
    
    merged_count = sum(1 for pr in prs if pr.get('merged'))
    
    labels = Counter()
    for pr in prs:
        for label in pr.get('labels', []):
            labels[label] += 1
    
    by_month = Counter()
    for pr in prs:
        try:
            dt = datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00'))
            month_key = dt.strftime('%Y-%m')
            by_month[month_key] += 1
        except:
            pass
    
    return {
        'total': len(prs),
        'states': dict(states),
        'open': states.get('open', 0),
        'closed': states.get('closed', 0),
        'merged': merged_count,
        'merge_rate': merged_count / len(prs) * 100 if prs else 0,
        'unique_authors': len(authors),
        'top_authors': top_authors,
        'labels': dict(labels.most_common(20)),
        'by_month': dict(sorted(by_month.items()))
    }


def analyze_issues(issues):
    """
    分析Issues数据
    """
    if not issues:
        return {}
    
    states = Counter(issue['state'] for issue in issues)
    
    authors = Counter(issue['author'] for issue in issues)
    
    labels = Counter()
    for issue in issues:
        for label in issue.get('labels', []):
            labels[label] += 1
    
    by_month = Counter()
    for issue in issues:
        try:
            dt = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
            month_key = dt.strftime('%Y-%m')
            by_month[month_key] += 1
        except:
            pass
    
    total_comments = sum(issue.get('comments', 0) for issue in issues)
    
    return {
        'total': len(issues),
        'states': dict(states),
        'open': states.get('open', 0),
        'closed': states.get('closed', 0),
        'close_rate': states.get('closed', 0) / len(issues) * 100 if issues else 0,
        'unique_authors': len(authors),
        'top_authors': authors.most_common(20),
        'labels': dict(labels.most_common(20)),
        'by_month': dict(sorted(by_month.items())),
        'total_comments': total_comments,
        'avg_comments': total_comments / len(issues) if issues else 0
    }


def save_analysis(data, filepath):
    """保存分析结果"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
