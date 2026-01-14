"""
高级AST分析 - 使用ast模块深度分析
"""
import ast
import os
from collections import defaultdict

class ComplexityVisitor(ast.NodeVisitor):
    """圈复杂度计算器"""
    
    def __init__(self):
        self.complexity = 1
    
    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)
    
    def visit_comprehension(self, node):
        self.complexity += 1
        self.generic_visit(node)

class FunctionAnalyzer(ast.NodeVisitor):
    """函数分析器"""
    
    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []
        self.decorators = []
        self.docstrings = []
    
    def visit_FunctionDef(self, node):
        func_info = {
            'name': node.name,
            'lineno': node.lineno,
            'end_lineno': getattr(node, 'end_lineno', node.lineno),
            'args': [arg.arg for arg in node.args.args],
            'num_args': len(node.args.args),
            'has_docstring': ast.get_docstring(node) is not None,
            'decorators': [ast.unparse(d) for d in node.decorator_list],
            'is_async': False,
            'complexity': self._calc_complexity(node)
        }
        self.functions.append(func_info)
        
        if ast.get_docstring(node):
            self.docstrings.append({
                'type': 'function',
                'name': node.name,
                'doc': ast.get_docstring(node)[:100]
            })
        
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        func_info = {
            'name': node.name,
            'lineno': node.lineno,
            'args': [arg.arg for arg in node.args.args],
            'num_args': len(node.args.args),
            'has_docstring': ast.get_docstring(node) is not None,
            'is_async': True,
            'complexity': self._calc_complexity(node)
        }
        self.functions.append(func_info)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
        class_info = {
            'name': node.name,
            'lineno': node.lineno,
            'methods': methods,
            'num_methods': len(methods),
            'bases': [ast.unparse(b) for b in node.bases],
            'has_docstring': ast.get_docstring(node) is not None
        }
        self.classes.append(class_info)
        self.generic_visit(node)
    
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
    
    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module)
    
    def _calc_complexity(self, node):
        visitor = ComplexityVisitor()
        visitor.visit(node)
        return visitor.complexity

def deep_analyze_file(filepath):
    """深度AST分析"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tree = ast.parse(source)
        analyzer = FunctionAnalyzer()
        analyzer.visit(tree)
        
        return {
            'filepath': filepath,
            'functions': analyzer.functions,
            'classes': analyzer.classes,
            'imports': analyzer.imports,
            'total_functions': len(analyzer.functions),
            'total_classes': len(analyzer.classes),
            'avg_complexity': sum(f['complexity'] for f in analyzer.functions) / len(analyzer.functions) if analyzer.functions else 0,
            'async_functions': len([f for f in analyzer.functions if f.get('is_async')])
        }
    except Exception as e:
        return {'error': str(e), 'filepath': filepath}

def analyze_project_ast(project_path):
    """分析整个项目的AST"""
    results = []
    stats = defaultdict(int)
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for f in files:
            if not f.endswith('.py'):
                continue
            
            filepath = os.path.join(root, f)
            analysis = deep_analyze_file(filepath)
            
            if 'error' not in analysis:
                results.append(analysis)
                stats['total_files'] += 1
                stats['total_functions'] += analysis['total_functions']
                stats['total_classes'] += analysis['total_classes']
    
    return {
        'files': results,
        'summary': dict(stats)
    }
