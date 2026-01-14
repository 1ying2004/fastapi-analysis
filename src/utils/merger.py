"""
数据合并器
"""
import json
import os

def merge_commit_data(files):
    """合并多个commit数据文件"""
    all_commits = []
    seen_hashes = set()
    
    for f in files:
        if not os.path.exists(f):
            continue
        
        with open(f, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
        
        for c in data:
            if c['hash'] not in seen_hashes:
                all_commits.append(c)
                seen_hashes.add(c['hash'])
    
    return all_commits

def merge_issues(files):
    """合并issue数据"""
    all_issues = []
    seen_numbers = set()
    
    for f in files:
        if not os.path.exists(f):
            continue
        
        with open(f, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
        
        for i in data:
            if i['number'] not in seen_numbers:
                all_issues.append(i)
                seen_numbers.add(i['number'])
    
    return all_issues
