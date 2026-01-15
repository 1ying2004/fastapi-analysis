"""
异常处理分析模块

分析代码中的异常处理模式
"""
import ast
import os


class ExceptionVisitor(ast.NodeVisitor):
    """异常处理访问器"""
    
    def __init__(self):
        self.try_blocks = 0
        self.except_handlers = []
        self.bare_excepts = 0
        self.finally_blocks = 0
    
    def visit_Try(self, node):
        self.try_blocks += 1
        
        for handler in node.handlers:
            if handler.type is None:
                self.bare_excepts += 1
            else:
                exc_name = handler.type.id if hasattr(handler.type, 'id') else str(handler.type)
                self.except_handlers.append(exc_name)
        
        if node.finalbody:
            self.finally_blocks += 1
        
        self.generic_visit(node)


def analyze_exceptions(filepath):
    """分析单个文件的异常处理"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except:
        return None
    
    visitor = ExceptionVisitor()
    visitor.visit(tree)
    
    return {
        'filepath': filepath,
        'try_blocks': visitor.try_blocks,
        'except_handlers': len(visitor.except_handlers),
        'bare_excepts': visitor.bare_excepts,
        'finally_blocks': visitor.finally_blocks,
        'exception_types': list(set(visitor.except_handlers))
    }


def analyze_project_exceptions(project_path):
    """分析整个项目的异常处理"""
    results = []
    summary = {
        'total_try_blocks': 0,
        'total_bare_excepts': 0,
        'total_finally_blocks': 0,
        'all_exception_types': set()
    }
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for f in files:
            if not f.endswith('.py'):
                continue
            
            filepath = os.path.join(root, f)
            result = analyze_exceptions(filepath)
            
            if result:
                results.append(result)
                summary['total_try_blocks'] += result['try_blocks']
                summary['total_bare_excepts'] += result['bare_excepts']
                summary['total_finally_blocks'] += result['finally_blocks']
                summary['all_exception_types'].update(result['exception_types'])
    
    summary['all_exception_types'] = list(summary['all_exception_types'])
    
    return {
        'files': results,
        'summary': summary
    }
