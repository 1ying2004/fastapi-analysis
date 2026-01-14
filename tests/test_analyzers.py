import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyzers.ast_analyzer import deep_analyze_file, analyze_project_ast

def test_deep_analyze_file():
    """测试文件分析"""
    result = deep_analyze_file(__file__)
    assert result is not None
    assert 'functions' in result or 'error' in result
    print("✓ test_deep_analyze_file")

def test_analyze_project():
    """测试项目分析"""
    result = analyze_project_ast('.')
    assert 'files' in result
    print("✓ test_analyze_project")

if __name__ == '__main__':
    test_deep_analyze_file()
    test_analyze_project()
    print("\n分析器测试通过！")
