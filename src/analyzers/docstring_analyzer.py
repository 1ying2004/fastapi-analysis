"""
文档字符串分析
"""
import ast

def extract_docstrings(filepath):
    """提取文件中的docstring"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except:
        return []
    
    docstrings = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
            ds = ast.get_docstring(node)
            if ds:
                name = getattr(node, 'name', 'module')
                docstrings.append({
                    'type': type(node).__name__,
                    'name': name,
                    'docstring': ds
                })
    
    return docstrings

def count_documented(filepath):
    """统计文档覆盖率"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except:
        return 0, 0
    
    total = 0
    documented = 0
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            total += 1
            if ast.get_docstring(node):
                documented += 1
    
    return documented, total
