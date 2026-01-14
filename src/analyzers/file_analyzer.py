"""
代码文件分析模块

分析Python文件的结构和内容
"""
import os
import ast


def analyze_file_structure(filepath):
    """
    分析单个文件结构
    
    Args:
        filepath: 文件路径
    
    Returns:
        文件结构信息字典
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        tree = ast.parse(content)
    except Exception as e:
        return {'error': str(e), 'filepath': filepath}
    
    functions = []
    classes = []
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                'name': node.name,
                'lineno': node.lineno,
                'args': len(node.args.args),
                'decorators': len(node.decorator_list)
            })
        elif isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            classes.append({
                'name': node.name,
                'lineno': node.lineno,
                'methods': methods,
                'bases': len(node.bases)
            })
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    
    return {
        'filepath': filepath,
        'lines': len(lines),
        'functions': functions,
        'classes': classes,
        'imports': imports,
        'function_count': len(functions),
        'class_count': len(classes),
        'import_count': len(imports)
    }


def scan_directory(path, extensions=None):
    """
    扫描目录获取所有文件
    
    Args:
        path: 目录路径
        extensions: 文件扩展名列表
    
    Returns:
        文件路径列表
    """
    if extensions is None:
        extensions = ['.py']
    
    files = []
    
    for root, dirs, filenames in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for f in filenames:
            if any(f.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, f))
    
    return files


def get_project_summary(path):
    """
    获取项目整体摘要
    """
    files = scan_directory(path)
    
    total_lines = 0
    total_functions = 0
    total_classes = 0
    
    for filepath in files:
        result = analyze_file_structure(filepath)
        if 'error' not in result:
            total_lines += result['lines']
            total_functions += result['function_count']
            total_classes += result['class_count']
    
    return {
        'total_files': len(files),
        'total_lines': total_lines,
        'total_functions': total_functions,
        'total_classes': total_classes
    }
