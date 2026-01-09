import libcst as cst

class CodeAnalyzer(cst.CSTVisitor):
    def __init__(self):
        self.imports = []
        self.functions = []
        self.classes = []
    
    def visit_Import(self, node):
        for name in node.names:
            if isinstance(name, cst.ImportAlias):
                self.imports.append(name.name.value)
    
    def visit_FunctionDef(self, node):
        self.functions.append(node.name.value)
    
    def visit_ClassDef(self, node):
        self.classes.append(node.name.value)

def analyze_with_libcst(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    tree = cst.parse_module(source)
    analyzer = CodeAnalyzer()
    tree.walk(analyzer)
    
    return {
        'imports': analyzer.imports,
        'functions': analyzer.functions,
        'classes': analyzer.classes
    }
