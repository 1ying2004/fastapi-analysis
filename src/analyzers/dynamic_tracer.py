import pysnooper

@pysnooper.snoop(output='trace.log')
def analyze_commits(commits):
    """分析提交数据"""
    authors = {}
    for commit in commits:
        author = commit['author']
        authors[author] = authors.get(author, 0) + 1
    
    return authors

@pysnooper.snoop()
def calculate_stats(data):
    """计算统计信息"""
    total = len(data)
    if total == 0:
        return {}
    
    return {
        'total': total,
        'unique': len(set(data))
    }

if __name__ == '__main__':
    demo_data = [{'author': 'A'}, {'author': 'B'}, {'author': 'A'}]
    result = analyze_commits(demo_data)
    print(f"结果: {result}")
