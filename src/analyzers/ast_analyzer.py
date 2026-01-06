import ast

def analyze_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tree = ast.parse(source)
        
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        return {
            'functions': functions,
            'classes': classes,
            'function_count': len(functions),
            'class_count': len(classes)
        }
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}")
        return None
