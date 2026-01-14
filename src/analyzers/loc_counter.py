"""
代码行数统计
"""
import os

def count_lines(filepath):
    """统计文件行数"""
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
    """分析项目代码行数"""
    results = {'total': 0, 'code': 0, 'blank': 0, 'comment': 0, 'files': 0}
    
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
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
