"""
代码依赖分析模块

分析Python文件之间的导入依赖关系
"""
import ast
import os
from collections import defaultdict


def extract_imports(filepath):
    """
    提取文件的所有导入
    
    Args:
        filepath: Python文件路径
    
    Returns:
        导入模块列表
    """
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
            if node.module:
                imports.append(node.module)
    
    return imports


def build_dependency_graph(project_path):
    """
    构建项目依赖图
    
    Args:
        project_path: 项目根目录
    
    Returns:
        依赖图字典
    """
    graph = defaultdict(set)
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for f in files:
            if not f.endswith('.py'):
                continue
            
            filepath = os.path.join(root, f)
            rel_path = os.path.relpath(filepath, project_path)
            imports = extract_imports(filepath)
            
            for imp in imports:
                graph[rel_path].add(imp)
    
    return dict(graph)


def find_circular_dependencies(graph):
    """
    检测循环依赖
    
    Args:
        graph: 依赖图
    
    Returns:
        循环依赖列表
    """
    visited = set()
    rec_stack = set()
    cycles = []
    
    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
        
        path.pop()
        rec_stack.remove(node)
    
    for node in graph:
        if node not in visited:
            dfs(node, [])
    
    return cycles


def get_most_imported(graph, top_n=10):
    """获取被导入最多的模块"""
    import_counts = defaultdict(int)
    
    for deps in graph.values():
        for dep in deps:
            import_counts[dep] += 1
    
    sorted_imports = sorted(import_counts.items(), key=lambda x: -x[1])
    return sorted_imports[:top_n]
