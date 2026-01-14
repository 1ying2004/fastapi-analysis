"""
JSON报告生成
"""
import json
import os
from datetime import datetime
from src.analyzers.stats import generate_report

def generate_json_report(commits, output_file='output/report.json'):
    """生成JSON格式报告"""
    stats = generate_report(commits)
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_commits': stats['total_commits'],
            'unique_authors': stats['unique_authors']
        },
        'author_stats': stats['author_stats'],
        'time_distribution': stats['time_distribution'],
        'message_types': stats['message_types']
    }
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✓ JSON报告: {output_file}")
    return report
