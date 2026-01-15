"""
API变更分析模块

分析代码中公共API的变更
"""
import ast
import os


def extract_public_api(filepath):
    """
    提取文件的公共API
    
    包括公共函数、类和常量
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except:
        return []
    
    api = []
    
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            if not node.name.startswith('_'):
                api.append({
                    'type': 'function',
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'lineno': node.lineno
                })
        
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith('_'):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and not item.name.startswith('_'):
                        methods.append(item.name)
                
                api.append({
                    'type': 'class',
                    'name': node.name,
                    'methods': methods,
                    'lineno': node.lineno
                })
        
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    api.append({
                        'type': 'constant',
                        'name': target.id,
                        'lineno': node.lineno
                    })
    
    return api


def analyze_project_api(project_path):
    """分析整个项目的公共API"""
    all_api = {}
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for f in files:
            if not f.endswith('.py'):
                continue
            
            filepath = os.path.join(root, f)
            api = extract_public_api(filepath)
            
            if api:
                rel_path = os.path.relpath(filepath, project_path)
                all_api[rel_path] = api
    
    return all_api


def get_api_summary(project_api):
    """获取API摘要"""
    total_functions = 0
    total_classes = 0
    total_constants = 0
    
    for apis in project_api.values():
        for item in apis:
            if item['type'] == 'function':
                total_functions += 1
            elif item['type'] == 'class':
                total_classes += 1
            elif item['type'] == 'constant':
                total_constants += 1
    
    return {
        'total_files': len(project_api),
        'public_functions': total_functions,
        'public_classes': total_classes,
        'public_constants': total_constants
    }
