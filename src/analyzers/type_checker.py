"""
类型注解检查
"""
import ast

def check_type_annotations(filepath):
    """检查类型注解"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except:
        return {'total': 0, 'annotated': 0}
    
    total_params = 0
    annotated_params = 0
    functions_with_return = 0
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # 检查参数注解
            for arg in node.args.args:
                total_params += 1
                if arg.annotation:
                    annotated_params += 1
            
            # 检查返回值注解
            if node.returns:
                functions_with_return += 1
    
    return {
        'total_params': total_params,
        'annotated_params': annotated_params,
        'functions_with_return': functions_with_return,
        'annotation_rate': annotated_params / total_params if total_params > 0 else 0
    }

def analyze_project_annotations(files):
    """分析项目整体注解情况"""
    total = {'total_params': 0, 'annotated_params': 0, 'functions_with_return': 0}
    
    for f in files:
        stats = check_type_annotations(f)
        total['total_params'] += stats['total_params']
        total['annotated_params'] += stats['annotated_params']
        total['functions_with_return'] += stats['functions_with_return']
    
    total['annotation_rate'] = (
        total['annotated_params'] / total['total_params']
        if total['total_params'] > 0 else 0
    )
    
    return total
