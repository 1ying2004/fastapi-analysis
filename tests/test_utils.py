import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.helpers import safe_divide, format_number, truncate_str

def test_safe_divide():
    """测试安全除法"""
    assert safe_divide(10, 2) == 5
    assert safe_divide(10, 0) == 0
    print("✓ test_safe_divide")

def test_format_number():
    """测试数字格式化"""
    assert format_number(1000) == "1,000"
    assert format_number(1234567) == "1,234,567"
    print("✓ test_format_number")

def test_truncate_str():
    """测试截断"""
    assert truncate_str("hello", 10) == "hello"
    result = truncate_str("a" * 100, 50)
    assert len(result) == 50
    print("✓ test_truncate_str")

if __name__ == '__main__':
    test_safe_divide()
    test_format_number()
    test_truncate_str()
    print("\nutils测试全部通过！")
