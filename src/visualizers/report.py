"""
报告生成模块
"""
import json
import os
from datetime import datetime
from src.analyzers.stats import generate_report

def generate_html_report(commits, output_file='output/report.html'):
    """生成HTML报告"""
    stats = generate_report(commits)
    
    html = f'''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>FastAPI 分析报告</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', sans-serif; margin: 40px; }}
        h1 {{ color: #667eea; }}
        .stat {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 10px 0; }}
        .number {{ font-size: 2em; color: #667eea; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>FastAPI 仓库分析报告</h1>
    <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="stat">
        <div class="number">{stats['total_commits']:,}</div>
        <div>总提交数</div>
    </div>
    
    <div class="stat">
        <div class="number">{stats['unique_authors']}</div>
        <div>贡献者数量</div>
    </div>
    
    <h2>提交类型分布</h2>
    <ul>
    {''.join(f"<li>{k}: {v}</li>" for k, v in stats['message_types'].items())}
    </ul>
</body>
</html>'''
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ HTML报告: {output_file}")
