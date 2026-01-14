"""
分支采集模块

获取Git仓库的分支信息。
"""
import subprocess


def get_branches(repo_path):
    """获取所有分支列表"""
    cmd = ['git', 'branch', '-a']
    try:
        output = subprocess.check_output(cmd, cwd=repo_path, encoding='utf-8')
    except:
        return []
    
    branches = []
    for line in output.strip().split('\n'):
        branch = line.strip().lstrip('* ')
        if branch:
            branches.append(branch)
    
    return branches


def get_current_branch(repo_path):
    """获取当前分支名"""
    cmd = ['git', 'branch', '--show-current']
    try:
        output = subprocess.check_output(cmd, cwd=repo_path, encoding='utf-8')
        return output.strip()
    except:
        return None


def get_branch_commits(repo_path, branch):
    """获取指定分支的提交数"""
    cmd = ['git', 'rev-list', '--count', branch]
    try:
        output = subprocess.check_output(cmd, cwd=repo_path, encoding='utf-8')
        return int(output.strip())
    except:
        return 0
