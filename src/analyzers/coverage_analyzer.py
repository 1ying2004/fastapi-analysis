"""
代码覆盖率分析模块

分析测试覆盖率相关数据
"""
import os
import ast


def estimate_test_coverage(project_path):
    """
    估算测试覆盖率
    
    通过分析tests目录和src目录的文件数量比例估算
    """
    src_files = 0
    test_files = 0
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for f in files:
            if f.endswith('.py'):
                if 'test' in root.lower() or f.startswith('test_'):
                    test_files += 1
                else:
                    src_files += 1
    
    if src_files == 0:
        return 0
    
    ratio = test_files / src_files * 100
    return min(ratio, 100)


def count_test_functions(project_path):
    """统计测试函数数量"""
    test_count = 0
    
    tests_dir = os.path.join(project_path, 'tests')
    if not os.path.exists(tests_dir):
        return 0
    
    for root, dirs, files in os.walk(tests_dir):
        for f in files:
            if f.endswith('.py') and f.startswith('test_'):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        tree = ast.parse(file.read())
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            if node.name.startswith('test_'):
                                test_count += 1
                except:
                    pass
    
    return test_count


def get_test_summary(project_path):
    """获取测试摘要"""
    return {
        'estimated_coverage': estimate_test_coverage(project_path),
        'test_function_count': count_test_functions(project_path)
    }
