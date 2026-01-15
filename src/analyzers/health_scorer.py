"""
项目健康度评分模块

综合评估项目健康状况
"""


def calculate_health_score(metrics):
    """
    计算项目健康度评分 (0-100)
    
    Args:
        metrics: 包含各项指标的字典
    
    Returns:
        健康度评分
    """
    score = 100
    
    total_commits = metrics.get('total_commits', 0)
    if total_commits < 100:
        score -= 10
    elif total_commits > 1000:
        score += 5
    
    contributors = metrics.get('contributors', 0)
    if contributors < 5:
        score -= 15
    elif contributors > 50:
        score += 10
    
    avg_complexity = metrics.get('avg_complexity', 1)
    if avg_complexity > 5:
        score -= 10
    elif avg_complexity < 2:
        score += 5
    
    test_coverage = metrics.get('test_coverage', 0)
    if test_coverage < 20:
        score -= 15
    elif test_coverage > 60:
        score += 10
    
    return max(0, min(100, score))


def get_health_grade(score):
    """根据分数获取等级"""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


def generate_health_report(metrics):
    """生成健康报告"""
    score = calculate_health_score(metrics)
    grade = get_health_grade(score)
    
    return {
        'score': score,
        'grade': grade,
        'metrics': metrics,
        'recommendations': get_recommendations(metrics)
    }


def get_recommendations(metrics):
    """根据指标生成改进建议"""
    recommendations = []
    
    if metrics.get('avg_complexity', 1) > 5:
        recommendations.append('建议降低函数复杂度')
    
    if metrics.get('test_coverage', 0) < 50:
        recommendations.append('建议增加测试覆盖率')
    
    if metrics.get('contributors', 0) < 3:
        recommendations.append('建议增加贡献者数量')
    
    return recommendations
