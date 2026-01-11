import libcst as cst
from typing import List, Dict

class CodeAnalyzer(cst.CSTVisitor):
    def __init__(self):
        self.imports: List[str] = []
        self.functions: List[str] = []
        self.classes: List[str] = []
        self.decorators: List[str] = []
    
    def visit_Import(self, node: cst.Import):
        for name in node.names:
            if isinstance(name, cst.ImportAlias):
                self.imports.append(cst.helpers.get_absolute_module(name.name))
    
    def visit_ImportFrom(self, node: cst.ImportFrom):
        if node.module:
            self.imports.append(cst.helpers.get_absolute_module(node.module))
    
    def visit_FunctionDef(self, node: cst.FunctionDef):
        self.functions.append(node.name.value)
    
    def visit_ClassDef(self, node: cst.ClassDef):
        self.classes.append(node.name.value)
    
    def visit_Decorator(self, node: cst.Decorator):
        self.decorators.append(str(node.decorator))

def analyze_with_libcst(filepath: str) -> Dict:
    """使用libcst分析代码"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tree = cst.parse_module(source)
        analyzer = CodeAnalyzer()
        tree.walk(analyzer)
        
        return {
            'imports': analyzer.imports,
            'functions': analyzer.functions,
            'classes': analyzer.classes,
            'decorators': analyzer.decorators
        }
    except Exception as e:
        print(f"libcst分析失败: {e}")
        return {}
