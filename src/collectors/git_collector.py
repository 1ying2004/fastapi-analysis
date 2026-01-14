"""
Git历史采集模块

本模块使用subprocess调用git命令获取仓库提交历史，
支持导出为CSV和JSON格式，用于后续分析和可视化。

主要功能：
- get_commits: 获取提交历史
- get_file_stats: 统计文件类型
- save_to_csv: 保存为CSV
- save_to_json: 保存为JSON
"""
import subprocess
from datetime import datetime
import pandas as pd
import json
import os


def get_commits(repo_path, max_count=10000):
    """
    获取Git仓库的提交历史记录
    
    Args:
        repo_path: 仓库路径
        max_count: 最大获取数量，默认10000
    
    Returns:
        提交记录列表，每条包含hash, author, email, date, message
    """
    # 构建git log命令，使用自定义格式
    cmd = ['git', 'log', f'--max-count={max_count}', 
           '--format=%H|%an|%ae|%ad|%s', '--date=iso']
    
    try:
        # 执行命令并获取输出
        output = subprocess.check_output(
            cmd, cwd=repo_path, encoding='utf-8', errors='replace'
        )
    except subprocess.CalledProcessError as e:
        print(f"git log失败: {e}")
        return []
    
    # 解析输出
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
    """
    统计仓库中各类型文件数量
    
    Args:
        repo_path: 仓库路径
    
    Returns:
        字典，key为扩展名，value为文件数量
    """
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
    """
    将提交记录保存为CSV文件
    
    Args:
        commits: 提交记录列表
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)
    df = pd.DataFrame(commits)
    df.to_csv(f'{output_dir}/commits.csv', index=False, encoding='utf-8-sig')
    print(f"✓ 保存CSV: {output_dir}/commits.csv")


def save_to_json(commits, output_dir='data'):
    """
    将提交记录保存为JSON文件
    
    Args:
        commits: 提交记录列表
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)
    with open(f'{output_dir}/commits.json', 'w', encoding='utf-8') as f:
        json.dump(commits, f, ensure_ascii=False, indent=2)
    print(f"✓ 保存JSON: {output_dir}/commits.json")
