"""
完整性检查
"""
import os

def check_project_structure(path):
    """检查项目结构完整性"""
    required = [
        'src',
        'src/collectors',
        'src/analyzers',
        'src/visualizers',
        'src/utils',
        'tests',
        'README.md',
        'requirements.txt'
    ]
    
    missing = []
    for item in required:
        full_path = os.path.join(path, item)
        if not os.path.exists(full_path):
            missing.append(item)
    
    return {
        'complete': len(missing) == 0,
        'missing': missing
    }

def check_imports():
    """检查关键导入"""
    results = {}
    
    modules = [
        ('pandas', 'pandas'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('wordcloud', 'wordcloud'),
        ('libcst', 'libcst'),
        ('z3', 'z3-solver')
    ]
    
    for name, pkg in modules:
        try:
            __import__(name)
            results[pkg] = True
        except ImportError:
            results[pkg] = False
    
    return results
