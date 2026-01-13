"""
依赖分析器 - 分析项目导入关系
"""
import ast
import os
from collections import defaultdict

def extract_imports(filepath):
    """提取文件的导入语句"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except:
        return []
    
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            imports.append(module)
    
    return imports

def build_dependency_graph(project_path):
    """构建依赖图"""
    graph = defaultdict(list)
    
    for root, _, files in os.walk(project_path):
        for f in files:
            if not f.endswith('.py'):
                continue
            
            filepath = os.path.join(root, f)
            rel_path = os.path.relpath(filepath, project_path)
            imports = extract_imports(filepath)
            
            for imp in imports:
                graph[rel_path].append(imp)
    
    return dict(graph)

def find_circular_deps(graph):
    """检测循环依赖"""
    # 简单实现
    circular = []
    for src, deps in graph.items():
        for dep in deps:
            if dep in graph and src in graph.get(dep, []):
                circular.append((src, dep))
    return circular
