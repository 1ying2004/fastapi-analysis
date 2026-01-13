"""
文件分析器 - 分析项目文件结构
"""
import os
from collections import defaultdict

def scan_directory(path, extensions=['.py']):
    """扫描目录获取文件列表"""
    files = []
    for root, dirs, filenames in os.walk(path):
        # 忽略隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for f in filenames:
            if any(f.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, f))
    
    return files

def get_line_counts(filepath):
    """统计文件行数"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        total = len(lines)
        blank = sum(1 for l in lines if not l.strip())
        comment = sum(1 for l in lines if l.strip().startswith('#'))
        code = total - blank - comment
        
        return {'total': total, 'code': code, 'blank': blank, 'comment': comment}
    except:
        return {'total': 0, 'code': 0, 'blank': 0, 'comment': 0}

def analyze_project(path):
    """分析整个项目"""
    files = scan_directory(path)
    results = []
    
    for f in files:
        stats = get_line_counts(f)
        stats['file'] = os.path.relpath(f, path)
        results.append(stats)
    
    return results
