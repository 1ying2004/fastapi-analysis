import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyzers.message_analyzer import categorize_commit, analyze_messages

def test_categorize_commit():
    """测试消息分类"""
    assert categorize_commit("feat: add feature") == "新功能"
    assert categorize_commit("fix: bug fix") == "修复"
    assert categorize_commit("docs: update") == "文档"
    assert categorize_commit("random message") == "其他"
    print("✓ test_categorize_commit")

def test_analyze_messages():
    """测试消息分析"""
    commits = [
        {'message': 'feat: a'},
        {'message': 'fix: b'},
        {'message': 'feat: c'}
    ]
    result = analyze_messages(commits)
    assert result['新功能'] == 2
    assert result['修复'] == 1
    print("✓ test_analyze_messages")

if __name__ == '__main__':
    test_categorize_commit()
    test_analyze_messages()
