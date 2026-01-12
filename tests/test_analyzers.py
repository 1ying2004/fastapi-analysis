import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyzers.ast_analyzer import analyze_file, calculate_complexity

def test_analyze_file():
    """测试文件分析"""
    # 分析自己
    result = analyze_file(__file__)
    assert result is not None
    assert 'functions' in result
    print("✓ test_analyze_file 通过")

def test_complexity():
    """测试复杂度计算"""
    complexity = calculate_complexity(__file__)
    assert complexity >= 1
    print(f"✓ test_complexity 通过 (复杂度: {complexity})")

if __name__ == '__main__':
    test_analyze_file()
    test_complexity()
    print("\n分析器测试通过！")
