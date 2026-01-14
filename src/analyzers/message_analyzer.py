"""
消息分析模块

分析Git提交消息，按类型分类，提取关键词。
"""
import re
from collections import Counter


def categorize_commit(message):
    """
    分类单条提交消息
    
    按conventional commits规范分类
    """
    msg = message.lower()
    
    if msg.startswith('feat'):
        return 'feature'
    elif msg.startswith('fix'):
        return 'bugfix'
    elif msg.startswith('docs'):
        return 'docs'
    elif msg.startswith('refactor'):
        return 'refactor'
    elif msg.startswith('test'):
        return 'test'
    elif msg.startswith('chore'):
        return 'chore'
    elif msg.startswith('style'):
        return 'style'
    elif msg.startswith('perf'):
        return 'perf'
    else:
        return 'other'


def analyze_messages(commits):
    """分析所有提交消息的类型分布"""
    categories = Counter()
    
    for c in commits:
        cat = categorize_commit(c['message'])
        categories[cat] += 1
    
    return dict(categories)


def extract_keywords(commits, top_n=20):
    """
    从提交消息中提取高频关键词
    
    Args:
        commits: 提交列表
        top_n: 返回top N个关键词
    """
    words = []
    for c in commits:
        msg = c['message']
        tokens = re.findall(r'\b[a-zA-Z]{3,}\b', msg.lower())
        words.extend(tokens)
    
    return Counter(words).most_common(top_n)
