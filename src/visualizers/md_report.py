"""
Markdown报告生成
"""
import os
from datetime import datetime
from src.analyzers.stats import generate_report

def generate_md_report(commits, output_file='output/report.md'):
    """生成Markdown格式报告"""
    stats = generate_report(commits)
    
    # 前10作者
    top_authors = list(stats['author_stats'].items())[:10]
    
    md = f'''# FastAPI 仓库分析报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 摘要

| 指标 | 数值 |
|------|------|
| 总提交数 | {stats['total_commits']:,} |
| 贡献者数 | {stats['unique_authors']} |

## Top 10 贡献者

| 排名 | 作者 | 提交数 |
|------|------|--------|
'''
    
    for i, (author, count) in enumerate(top_authors, 1):
        md += f'| {i} | {author} | {count} |\n'
    
    md += '''
## 提交类型分布

| 类型 | 数量 |
|------|------|
'''
    
    for t, count in stats['message_types'].items():
        md += f'| {t} | {count} |\n'
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md)
    
    print(f"✓ Markdown报告: {output_file}")
