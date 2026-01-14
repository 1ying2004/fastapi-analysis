import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.helpers import safe_divide, percentage, truncate

def test_safe_divide():
    """测试安全除法"""
    assert safe_divide(10, 2) == 5
    assert safe_divide(10, 0) == 0
    print("✓ test_safe_divide")

def test_percentage():
    """测试百分比"""
    assert percentage(50, 100) == 50
    assert percentage(0, 100) == 0
    print("✓ test_percentage")

def test_truncate():
    """测试截断"""
    assert truncate("hello", 10) == "hello"
    assert len(truncate("a" * 100, 50)) == 50
    print("✓ test_truncate")

if __name__ == '__main__':
    test_safe_divide()
    test_percentage()
    test_truncate()
    print("\nutils测试全部通过！")
