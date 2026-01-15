"""
项目健康度评分模块

综合评估项目质量，给出合理评分
"""


def calculate_health_score(metrics):
    """
    计算项目健康度评分 (0-100)
    
    评分维度：
    - 提交活跃度 (20分)
    - 贡献者多样性 (20分)
    - 代码复杂度 (20分)
    - Issue处理率 (20分)
    - PR合并率 (20分)
    """
    score = 0
    details = {}
    
    total_commits = metrics.get('total_commits', 0)
    if total_commits >= 5000:
        commit_score = 20
    elif total_commits >= 1000:
        commit_score = 15
    elif total_commits >= 500:
        commit_score = 10
    elif total_commits >= 100:
        commit_score = 5
    else:
        commit_score = 2
    score += commit_score
    details['提交活跃度'] = f"{commit_score}/20"
    
    contributors = metrics.get('contributors', 0)
    if contributors >= 500:
        contrib_score = 20
    elif contributors >= 100:
        contrib_score = 15
    elif contributors >= 50:
        contrib_score = 10
    elif contributors >= 10:
        contrib_score = 5
    else:
        contrib_score = 2
    score += contrib_score
    details['贡献者多样性'] = f"{contrib_score}/20"
    
    avg_complexity = metrics.get('avg_complexity', 5)
    if avg_complexity <= 2:
        complex_score = 20
    elif avg_complexity <= 4:
        complex_score = 15
    elif avg_complexity <= 6:
        complex_score = 10
    elif avg_complexity <= 10:
        complex_score = 5
    else:
        complex_score = 2
    score += complex_score
    details['代码复杂度'] = f"{complex_score}/20 (avg={avg_complexity:.2f})"
    
    issue_close_rate = metrics.get('issue_close_rate', 50)
    if issue_close_rate >= 80:
        issue_score = 20
    elif issue_close_rate >= 60:
        issue_score = 15
    elif issue_close_rate >= 40:
        issue_score = 10
    else:
        issue_score = 5
    score += issue_score
    details['Issue处理率'] = f"{issue_score}/20 ({issue_close_rate:.1f}%)"
    
    pr_merge_rate = metrics.get('pr_merge_rate', 50)
    if pr_merge_rate >= 70:
        pr_score = 20
    elif pr_merge_rate >= 50:
        pr_score = 15
    elif pr_merge_rate >= 30:
        pr_score = 10
    else:
        pr_score = 5
    score += pr_score
    details['PR合并率'] = f"{pr_score}/20 ({pr_merge_rate:.1f}%)"
    
    return score, details


def get_health_grade(score):
    """根据分数获取等级"""
    if score >= 90:
        return 'A', '优秀'
    elif score >= 80:
        return 'B', '良好'
    elif score >= 70:
        return 'C', '中等'
    elif score >= 60:
        return 'D', '及格'
    else:
        return 'F', '需改进'


def generate_health_report(metrics):
    """生成健康报告"""
    score, details = calculate_health_score(metrics)
    grade, grade_name = get_health_grade(score)
    
    return {
        'score': score,
        'grade': grade,
        'grade_name': grade_name,
        'details': details,
        'metrics': metrics,
        'recommendations': get_recommendations(metrics, score)
    }


def get_recommendations(metrics, score):
    """根据指标生成改进建议"""
    recommendations = []
    
    if metrics.get('avg_complexity', 1) > 5:
        recommendations.append('建议重构高复杂度函数')
    
    if metrics.get('contributors', 0) < 10:
        recommendations.append('建议吸引更多贡献者参与')
    
    if metrics.get('issue_close_rate', 100) < 50:
        recommendations.append('建议加快Issue处理速度')
    
    if metrics.get('pr_merge_rate', 100) < 50:
        recommendations.append('建议优化PR审核流程')
    
    if score >= 80:
        recommendations.append('项目状态良好，继续保持!')
    
    return recommendations
