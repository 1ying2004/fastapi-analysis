import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collectors.git_collector import get_commits

@pytest.mark.skipif(not os.path.exists('.git'), reason="需要git仓库")
def test_get_commits():
    """测试获取提交 - 用当前仓库"""
    commits = get_commits('.', max_count=10)
    assert len(commits) > 0
    assert 'hash' in commits[0]
    assert 'author' in commits[0]
    print("✓ test_get_commits 通过")

@pytest.mark.skipif(not os.path.exists('.git'), reason="需要git仓库")
def test_commit_fields():
    """测试字段完整性"""
    commits = get_commits('.', max_count=5)
    required_fields = ['hash', 'author', 'email', 'date', 'message']
    for c in commits:
        for field in required_fields:
            assert field in c, f"缺少字段: {field}"
    print("✓ test_commit_fields 通过")

if __name__ == '__main__':
    test_get_commits()
    test_commit_fields()
    print("\n所有测试通过！")
