"""
libcst高级代码分析器
实际使用libcst进行代码结构分析和代码变换
"""
import libcst as cst
from libcst import matchers as m
from typing import List, Dict, Set
import os

class ImportCollector(cst.CSTVisitor):
    """收集所有导入"""
    
    def __init__(self):
        self.imports: List[str] = []
        self.from_imports: Dict[str, List[str]] = {}
    
    def visit_Import(self, node: cst.Import) -> None:
        for name in node.names:
            if isinstance(name, cst.ImportAlias):
                self.imports.append(name.name.value if hasattr(name.name, 'value') else str(name.name))
    
    def visit_ImportFrom(self, node: cst.ImportFrom) -> None:
        if node.module:
            module_name = node.module.value if hasattr(node.module, 'value') else str(node.module)
            names = []
            if isinstance(node.names, cst.ImportStar):
                names = ['*']
            elif node.names:
                for name in node.names:
                    if isinstance(name, cst.ImportAlias):
                        names.append(name.name.value)
            self.from_imports[module_name] = names

class FunctionCollector(cst.CSTVisitor):
    """收集函数和方法信息"""
    
    def __init__(self):
        self.functions: List[Dict] = []
        self.current_class: str = None
    
    def visit_ClassDef(self, node: cst.ClassDef) -> None:
        self.current_class = node.name.value
    
    def leave_ClassDef(self, node: cst.ClassDef) -> None:
        self.current_class = None
    
    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        func_info = {
            'name': node.name.value,
            'class': self.current_class,
            'is_method': self.current_class is not None,
            'params': [],
            'decorators': [],
            'is_async': False,
            'has_return_annotation': node.returns is not None
        }
        
        for param in node.params.params:
            param_info = {'name': param.name.value}
            if param.annotation:
                param_info['type'] = True
            func_info['params'].append(param_info)
        
        for decorator in node.decorators:
            if hasattr(decorator.decorator, 'value'):
                func_info['decorators'].append(decorator.decorator.value)
        
        self.functions.append(func_info)

class ClassAnalyzer(cst.CSTVisitor):
    """类继承和结构分析"""
    
    def __init__(self):
        self.classes: List[Dict] = []
    
    def visit_ClassDef(self, node: cst.ClassDef) -> None:
        bases = []
        for base in node.bases:
            if hasattr(base.value, 'value'):
                bases.append(base.value.value)
        
        methods = []
        attributes = []
        
        for stmt in node.body.body:
            if isinstance(stmt, cst.FunctionDef):
                methods.append(stmt.name.value)
            elif isinstance(stmt, cst.SimpleStatementLine):
                for s in stmt.body:
                    if isinstance(s, (cst.Assign, cst.AnnAssign)):
                        attributes.append('attribute')
        
        self.classes.append({
            'name': node.name.value,
            'bases': bases,
            'methods': methods,
            'num_methods': len(methods),
            'decorators': [d.decorator.value for d in node.decorators if hasattr(d.decorator, 'value')]
        })

def analyze_with_libcst(filepath: str) -> Dict:
    """使用libcst进行完整分析"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tree = cst.parse_module(source)
        
        import_collector = ImportCollector()
        tree.walk(import_collector)
        
        func_collector = FunctionCollector()
        tree.walk(func_collector)
        
        class_analyzer = ClassAnalyzer()
        tree.walk(class_analyzer)
        
        return {
            'filepath': filepath,
            'imports': import_collector.imports,
            'from_imports': import_collector.from_imports,
            'functions': func_collector.functions,
            'classes': class_analyzer.classes,
            'total_imports': len(import_collector.imports) + len(import_collector.from_imports),
            'total_functions': len(func_collector.functions),
            'total_classes': len(class_analyzer.classes)
        }
    except Exception as e:
        return {'error': str(e), 'filepath': filepath}

def analyze_project_libcst(project_path: str) -> Dict:
    """分析整个项目"""
    results = []
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for f in files:
            if not f.endswith('.py'):
                continue
            
            filepath = os.path.join(root, f)
            result = analyze_with_libcst(filepath)
            if 'error' not in result:
                results.append(result)
    
    return {
        'files': results,
        'total_files': len(results)
    }
