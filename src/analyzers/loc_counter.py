"""
代码行数统计模块

统计Python项目的代码行数、空行数和注释行数。
"""
import os


def count_lines(filepath):
    """
    统计单个文件的行数
    
    Args:
        filepath: 文件路径
    
    Returns:
        包含total, code, blank, comment的字典
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        total = len(lines)
        blank = sum(1 for l in lines if not l.strip())
        comment = sum(1 for l in lines if l.strip().startswith('#'))
        code = total - blank - comment
        
        return {
            'file': filepath,
            'total': total,
            'code': code,
            'blank': blank,
            'comment': comment
        }
    except:
        return None


def analyze_project_loc(path):
    """
    分析整个项目的代码行数
    
    Args:
        path: 项目根目录
    
    Returns:
        项目整体行数统计
    """
    results = {'total': 0, 'code': 0, 'blank': 0, 'comment': 0, 'files': 0}
    
    for root, dirs, files in os.walk(path):
        # 排除隐藏目录和缓存
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for f in files:
            if not f.endswith('.py'):
                continue
            
            filepath = os.path.join(root, f)
            stats = count_lines(filepath)
            
            if stats:
                results['total'] += stats['total']
                results['code'] += stats['code']
                results['blank'] += stats['blank']
                results['comment'] += stats['comment']
                results['files'] += 1
    
    return results
