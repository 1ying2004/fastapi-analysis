import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyzers.message_analyzer import categorize_commit, analyze_messages

def test_categorize_commit():
    """测试消息分类"""
    assert categorize_commit("feat: add feature") == "feature"
    assert categorize_commit("fix: bug fix") == "bugfix"
    assert categorize_commit("docs: update") == "docs"
    assert categorize_commit("random message") == "other"
    print("✓ test_categorize_commit")

def test_analyze_messages():
    """测试消息分析"""
    commits = [
        {'message': 'feat: a'},
        {'message': 'fix: b'},
        {'message': 'feat: c'}
    ]
    result = analyze_messages(commits)
    assert result['feature'] == 2
    assert result['bugfix'] == 1
    print("✓ test_analyze_messages")

if __name__ == '__main__':
    test_categorize_commit()
    test_analyze_messages()
