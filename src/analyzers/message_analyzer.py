"""
消息分析模块

分析Git提交消息，按类型分类，提取关键词。
"""
import re
from collections import Counter


COMMIT_PATTERNS = [
    (r'^feat[\(:]|^feature[\(:]|add\s|添加', '新功能'),
    (r'^fix[\(:]|^bugfix[\(:]|修复|修正', '修复'),
    (r'^docs[\(:]|^doc[\(:]|文档|readme', '文档'),
    (r'^refactor[\(:]|重构', '重构'),
    (r'^test[\(:]|测试', '测试'),
    (r'^chore[\(:]|^build[\(:]|^ci[\(:]', '构建/CI'),
    (r'^style[\(:]|格式|样式', '样式'),
    (r'^perf[\(:]|性能|优化', '性能'),
    (r'upgrade|update|bump|升级|更新', '依赖更新'),
    (r'merge|合并', '合并'),
    (r'revert|回滚', '回滚'),
    (r'release|发布', '发布'),
]


def categorize_commit(message):
    """
    分类单条提交消息
    
    使用正则匹配多种模式
    """
    msg = message.lower()
    
    for pattern, category in COMMIT_PATTERNS:
        if re.search(pattern, msg, re.IGNORECASE):
            return category
    
    return '其他'


def analyze_messages(commits):
    """分析所有提交消息的类型分布"""
    categories = Counter()
    
    for c in commits:
        cat = categorize_commit(c['message'])
        categories[cat] += 1
    
    sorted_cats = dict(sorted(categories.items(), key=lambda x: -x[1]))
    return sorted_cats


def get_message_stats(commits):
    """获取消息统计详情"""
    categories = analyze_messages(commits)
    total = sum(categories.values())
    
    stats = {
        'total': total,
        'categories': categories,
        'percentages': {k: v/total*100 for k, v in categories.items()}
    }
    return stats


def extract_keywords(commits, top_n=30):
    """
    从提交消息中提取高频关键词
    """
    words = []
    stop_words = {'the', 'and', 'for', 'from', 'with', 'this', 'that', 'are', 'was', 'were'}
    
    for c in commits:
        msg = c['message']
        tokens = re.findall(r'\b[a-zA-Z]{4,}\b', msg.lower())
        words.extend([t for t in tokens if t not in stop_words])
    
    return Counter(words).most_common(top_n)
