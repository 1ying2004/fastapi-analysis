"""
Git差异分析
"""
import subprocess

def get_commit_diff(repo_path, commit_hash):
    """获取提交的diff"""
    cmd = ['git', 'show', commit_hash, '--stat']
    try:
        output = subprocess.check_output(cmd, cwd=repo_path, encoding='utf-8', errors='replace')
        return output
    except:
        return None

def get_changed_files(repo_path, commit_hash):
    """获取变更的文件列表"""
    cmd = ['git', 'show', commit_hash, '--name-only', '--format=']
    try:
        output = subprocess.check_output(cmd, cwd=repo_path, encoding='utf-8')
        return [f.strip() for f in output.strip().split('\n') if f.strip()]
    except:
        return []

def get_insertions_deletions(repo_path, commit_hash):
    """获取增删行数"""
    cmd = ['git', 'show', commit_hash, '--numstat', '--format=']
    try:
        output = subprocess.check_output(cmd, cwd=repo_path, encoding='utf-8')
        insertions = 0
        deletions = 0
        
        for line in output.strip().split('\n'):
            parts = line.split('\t')
            if len(parts) >= 2:
                try:
                    insertions += int(parts[0]) if parts[0] != '-' else 0
                    deletions += int(parts[1]) if parts[1] != '-' else 0
                except:
                    pass
        
        return insertions, deletions
    except:
        return 0, 0
