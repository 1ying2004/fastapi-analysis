"""
代码质量指标
"""
import os
from src.analyzers.loc_counter import count_lines
from src.analyzers.docstring_analyzer import count_documented
from src.analyzers.type_checker import check_type_annotations

def calculate_quality_score(filepath):
    """计算单文件质量分数"""
    score = 100
    
    # 行数统计
    loc = count_lines(filepath)
    if loc and loc['total'] > 500:
        score -= 10
    
    # 文档覆盖率
    doc, total = count_documented(filepath)
    if total > 0:
        doc_rate = doc / total
        score += doc_rate * 20
    
    # 类型注解
    types = check_type_annotations(filepath)
    if types['annotation_rate'] > 0.5:
        score += 15
    
    return min(100, max(0, score))

def analyze_project_quality(path):
    """分析项目整体质量"""
    scores = []
    
    for root, _, files in os.walk(path):
        for f in files:
            if not f.endswith('.py'):
                continue
            
            filepath = os.path.join(root, f)
            score = calculate_quality_score(filepath)
            scores.append({
                'file': filepath,
                'score': score
            })
    
    if scores:
        avg = sum(s['score'] for s in scores) / len(scores)
    else:
        avg = 0
    
    return {
        'files': scores,
        'average_score': avg
    }
