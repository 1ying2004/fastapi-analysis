"""
代码风格检查模块

分析代码风格和规范性
"""
import os
import re


def check_naming_conventions(filepath):
    """
    检查命名规范
    
    检查变量、函数、类的命名是否符合PEP8规范
    """
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return issues
    
    for i, line in enumerate(lines, 1):
        if re.match(r'^class\s+[a-z]', line):
            issues.append({
                'line': i,
                'type': 'class_naming',
                'message': '类名应使用CamelCase'
            })
        
        if re.match(r'^def\s+[A-Z]', line):
            issues.append({
                'line': i,
                'type': 'function_naming',
                'message': '函数名应使用snake_case'
            })
    
    return issues


def check_line_length(filepath, max_length=120):
    """检查行长度"""
    long_lines = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return long_lines
    
    for i, line in enumerate(lines, 1):
        if len(line.rstrip()) > max_length:
            long_lines.append({
                'line': i,
                'length': len(line.rstrip())
            })
    
    return long_lines


def analyze_code_style(project_path):
    """分析整个项目的代码风格"""
    results = {
        'files_checked': 0,
        'naming_issues': 0,
        'long_lines': 0
    }
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for f in files:
            if not f.endswith('.py'):
                continue
            
            filepath = os.path.join(root, f)
            results['files_checked'] += 1
            results['naming_issues'] += len(check_naming_conventions(filepath))
            results['long_lines'] += len(check_line_length(filepath))
    
    return results
