import subprocess
from datetime import datetime
import pandas as pd
import json
import os

def get_commits(repo_path, max_count=10000):
    """获取所有提交记录"""
    cmd = ['git', 'log', f'--max-count={max_count}', 
           '--format=%H|%an|%ae|%ad|%s', '--date=iso']
    
    try:
        output = subprocess.check_output(
            cmd, cwd=repo_path, encoding='utf-8', errors='replace'
        )
    except subprocess.CalledProcessError as e:
        print(f"git log失败: {e}")
        return []
    
    commits = []
    for line in output.strip().split('\n'):
        if '|' not in line:
            continue
        parts = line.split('|', 4)
        if len(parts) < 5:
            continue
        
        hash_val, author, email, date, msg = parts
        commits.append({
            'hash': hash_val,
            'author': author,
            'email': email,
            'date': date,
            'message': msg
        })
    
    print(f"✓ 获取 {len(commits)} 条提交")
    return commits

def get_file_stats(repo_path):
    """统计文件类型"""
    cmd = ['git', 'ls-files']
    try:
        output = subprocess.check_output(cmd, cwd=repo_path, encoding='utf-8')
    except:
        return {}
    
    stats = {}
    for file in output.strip().split('\n'):
        ext = os.path.splitext(file)[1] or 'no_ext'
        stats[ext] = stats.get(ext, 0) + 1
    
    return stats

def save_to_csv(commits, output_dir='data'):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.DataFrame(commits)
    df.to_csv(f'{output_dir}/commits.csv', index=False, encoding='utf-8-sig')
    print(f"✓ 保存CSV: {output_dir}/commits.csv")

def save_to_json(commits, output_dir='data'):
    os.makedirs(output_dir, exist_ok=True)
    with open(f'{output_dir}/commits.json', 'w', encoding='utf-8') as f:
        json.dump(commits, f, ensure_ascii=False, indent=2)
    print(f"✓ 保存JSON: {output_dir}/commits.json")
